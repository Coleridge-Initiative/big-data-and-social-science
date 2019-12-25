"""Creating Labels

Script for running steps in 1_Machine_Learning_Labels.ipynb

"""

# Setup

import pandas as pd
import sqlite3
from dateutil.parser import parse

# Define create_labels function

def create_labels(features_end, prediction_start, prediction_end, conn, output = False):
    """
    Generate a list of labels and return the table as a dataframe.
    
    Parameters
    ----------
    features_end
    prediction_start
    prediction_end
    conn: obj
        
    Returns
    -------
    df_labels: DataFrame
    """
    end_x_year = parse(features_end, fuzzy = True).year
    start_y_year = parse(prediction_start, fuzzy = True).year
    end_y_year = parse(prediction_end, fuzzy = True).year
    
    sql_script="""

    drop table if exists sentences_prep;
    create table sentences_prep as
    select inmate_doc_number, 
    cast(inmate_sentence_component as integer) as sentence_component,
    date([sentence_begin_date_(for_max)]) as sentence_begin_date,
    date(actual_sentence_end_date) as sentence_end_date
    from sentences;

    drop table if exists release_dates_2000_{end_x_year};
    create temp table release_dates_2000_{end_x_year} as
    select inmate_doc_number, sentence_end_date
    from sentences_prep
    where sentence_end_date >= '2000-01-01' and sentence_end_date <= '{features_end}';

    drop table if exists last_exit_2000_{end_x_year};
    create temp table last_exit_2000_{end_x_year} as
    select inmate_doc_number, max(sentence_end_date) sentence_end_date
    from release_dates_2000_{end_x_year}
    group by inmate_doc_number;

    drop table if exists admit_{start_y_year}_{end_y_year};
    create temp table admit_{start_y_year}_{end_y_year} as
    select inmate_doc_number, sentence_component, sentence_begin_date
    from sentences_prep
    where sentence_begin_date >= '{prediction_start}' and sentence_begin_date <= '{prediction_end}' and sentence_component = 1;

    drop table if exists recidivism_{start_y_year}_{end_y_year};
    create temp table recidivism_{start_y_year}_{end_y_year} as
    select r.inmate_doc_number, r.sentence_end_date, a.sentence_begin_date,
    case when a.sentence_begin_date is null then 0 else 1 end recidivism
    from last_exit_2000_{end_x_year} r
    left join admit_{start_y_year}_{end_y_year} a on r.inmate_doc_number = a.inmate_doc_number;

    drop table if exists recidivism_labels_{start_y_year}_{end_y_year};
    create table recidivism_labels_{start_y_year}_{end_y_year} as
    select distinct inmate_doc_number, recidivism
    from recidivism_{start_y_year}_{end_y_year};

    """.format(features_end = features_end,
               prediction_start = prediction_start,
               prediction_end = prediction_end,
               end_x_year = end_x_year,
               start_y_year = start_y_year,
               end_y_year = end_y_year)
       
    cur = conn.cursor()
    
    try:
        cur.executescript(sql_script)
        cur.close()
        conn.commit()
    except:
        conn.rollback()
        
    if output:
        df_label = pd.read_sql('select * from recidivism_labels_{start_y_year}_{end_y_year}'.format(
                                                                                        start_y_year = start_y_year,
                                                                                        end_y_year = end_y_year), conn)    
        return df_label
    else:
        print('Labels table ({pred_start} to {pred_end}) created. Use output = True to get a DataFrame as the output.'.format(pred_start = prediction_start,
                                                                                                                                                pred_end = prediction_end))


# Run create_labels function
if __name__ == '__main__':
    DB = 'ncdoc.db'
    conn = sqlite3.connect(DB)
    
    create_labels('2008-12-31', '2009-01-01', '2013-12-31', conn)
    create_labels('2013-12-31', '2014-01-01', '2018-12-31', conn)


