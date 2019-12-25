"""Creating Features

Script for running steps in 2_Machine_Learning_Features.ipynb

"""

# Setup

import pandas as pd
import sqlite3
from dateutil.parser import parse

# Define create_features function

def create_features(features_end, prediction_start, prediction_end, conn, output = False):
    """
    Generate a list of features and return the table as a dataframe.
    Note: There has to be a table of labels that correspond with the same time period. 
    
    Parameters
    ----------
    features_end
    prediction_start
    prediction_end
    conn: obj
        
    Returns
    -------
    df_features: Dataframe
    """
    end_x_year = parse(features_end, fuzzy=True).year
    start_y_year = parse(prediction_start, fuzzy=True).year
    end_y_year = parse(prediction_end, fuzzy=True).year 
    
    sql_script="""

    drop table if exists sentences_prep;
    create table sentences_prep as
    select inmate_doc_number, 
    cast(inmate_sentence_component as integer) as sentence_component,
    date([sentence_begin_date_(for_max)]) as sentence_begin_date,
    date(actual_sentence_end_date) as sentence_end_date
    from sentences;

    drop table if exists feature_num_admits_2000_{end_x_year};
    create table feature_num_admits_2000_{end_x_year} as
    select inmate_doc_number, count(*) num_admits
    from sentences_prep
    where inmate_doc_number in (select inmate_doc_number from recidivism_labels_{start_y_year}_{end_y_year})
    and sentence_begin_date < '{features_end}' and sentence_component = 1
    group by inmate_doc_number;

    drop table if exists feature_length_sentence_2000_{end_x_year};
    create table feature_length_sentence_2000_{end_x_year} as
    select inmate_doc_number, sentence_component, cast(julianday(sentence_end_date) - julianday(sentence_begin_date) as integer) length_sentence
    from sentences_prep
    where inmate_doc_number in (select inmate_doc_number from recidivism_labels_{start_y_year}_{end_y_year})
    and sentence_begin_date < '{features_end}' and sentence_component = 1
    and sentence_begin_date > '0001-01-01' and sentence_end_date > '0001-01-01' and sentence_end_date > sentence_begin_date;

    drop table if exists feature_length_long_sentence_2000_{end_x_year};
    create temp table feature_length_long_sentence_2000_{end_x_year} as
    select inmate_doc_number, max(length_sentence) length_longest_sentence
    from feature_length_sentence_2000_{end_x_year}
    group by inmate_doc_number;

    drop table if exists docnbr_admityr;
    create temp table docnbr_admityr as
    select inmate_doc_number, min(sentence_begin_date) min_admityr
    from sentences_prep
    where sentence_begin_date > '0001-01-01'
    group by inmate_doc_number;

    drop table if exists age_first_admit_birth_year;
    create temp table age_first_admit_birth_year as
    select da.inmate_doc_number,
    cast(strftime("%Y", da.min_admityr) as integer) min_admityr,
    cast(strftime("%Y", p.inmate_birth_date) as integer) inmate_birth_date
    from docnbr_admityr da
    left join inmate p on da.inmate_doc_number = p.inmate_doc_number;

    drop table if exists feature_age_first_admit; 
    create table feature_age_first_admit as
    select inmate_doc_number, (min_admityr - inmate_birth_date) age_first_admit
    from age_first_admit_birth_year;

    drop table if exists feature_agefirstadmit; 
    create table feature_agefirstadmit as
    select inmate_doc_number, age_first_admit
    from feature_age_first_admit
    where inmate_doc_number in (select inmate_doc_number from recidivism_labels_{start_y_year}_{end_y_year});

    drop table if exists feature_age_{end_x_year}; 
    create table feature_age_{end_x_year} as
    select inmate_doc_number, ({end_x_year} - cast(strftime("%Y", inmate_birth_date) as integer)) age
    from inmate
    where inmate_doc_number in (select inmate_doc_number from recidivism_labels_{start_y_year}_{end_y_year});

    drop table if exists features_2000_{end_x_year}; 
    create table features_2000_{end_x_year} as
    select f1.inmate_doc_number, f1.num_admits, f2.length_longest_sentence, f3.age_first_admit, f4.age
    from feature_num_admits_2000_{end_x_year} f1
    left join feature_length_long_sentence_2000_{end_x_year} f2 on f1.inmate_doc_number = f2.inmate_doc_number
    left join feature_agefirstadmit f3 on f1.inmate_doc_number = f3.inmate_doc_number
    left join feature_age_{end_x_year} f4 on f1.inmate_doc_number = f4.inmate_doc_number;

    """.format(features_end = features_end,
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
        df_features = pd.read_sql('select * from features_2000_{end_x_year}'.format(end_x_year = end_x_year), conn)    
        return df_features
    else:
         print('Features table ({pred_start} to {pred_end}) created. Use output = True to get a DataFrame as the output.'.format(pred_start = prediction_start, 
                                                                                                                                                   pred_end = prediction_end))

# Run create_features function
if __name__ == '__main__':
    DB = 'ncdoc.db'
    conn = sqlite3.connect(DB)
    
    create_features('2008-12-31', '2009-01-01', '2013-12-31', conn)
    create_features('2013-12-31', '2014-01-01', '2018-12-31', conn)

