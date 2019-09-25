Workbooks {#chap:workbooks}
=========

**Jonathan Scott Morgan, Christina Jones, and Ahmad Emad**


This final chapter provides an overview of the Python workbooks that
accompany each chapter. These workbooks combine text explanation and
code you can run, implemented in *Jupyter notebooks*^[See jupyter.org], to explain techniques and approaches
selected from each chapter and to provide thorough implementation
details, enabling students and interested practitioners to quickly get
up to speed on and start using the technologies covered in the book. We
hope you have a lot of fun with them.

Introduction
------------

We provide accompanying Juptyer IPython workbooks for mostchapters in
this book. These workbooks explain techniques and approaches selected
from each chapter and provide thorough implementation details so that
students and interested practitioners can quickly start using the
technologies covered within.

The workbooks and related files are stored in the *Big-Data-Workbooks GitHub repository*^[github.com/BigDataSocialScience], and so are freely available to be downloaded by anyone at any time and run on any
appropriately configured computer. These workbooks are a live set of
documents that could potentially change over time, so see the repository
for the most recent set of information.

These workbooks provide a thorough overview of the work needed to
implement the selected technologies. They combine explanation, basic
exercises, and substantial additional Python code to provide a
conceptual understanding of each technology, give insight into how key
parts of the process are implemented through exercises, and then lay out
an end-to-end pattern for implementing each in your own work. The
workbooks are implemented using IPython notebooks, interactive documents
that mix formatted text and Python code samples that can be edited and
run in real time in a Jupyter notebook server, allowing you to run and
explore the code for each technology as you read about it.

Environment
-----------

The Big-Data-Workbooks GitHub repository provides two different types of
workbooks, each needing a different Python setup to run. The first type
of workbooks is intended to be downloaded andrun locally by individual
users. The second type is designed to be hosted, assigned, worked on,
and graded on a single server, using `jupyterhub` (<https://github.com/jupyter/jupyterhub>) to hostand run the notebooks and `nbgrader` (<https://github.com/jupyter/nbgrader>) to assign, collect, and grade.

The text, images, and Python code in the workbooks are the same between
the two versions, as are the files and programs needed to complete each.

The differences in the workbooks themselves relate to the code cells
within each notebook where users implement and test exercises. In the
workbooks intended to be used locally, exercises are implemented in
simple interactive code cells. In the `nbgrader` versions, these cells have
additional metadata and contain the solutions for the exercises, making
them a convenient answer key even if you are working on them locally.

### Running workbooks locally

To run workbooks locally, you will need to install Python on your
system, then install `ipython`, which includes a local Jupyter server you can use
to run the workbooks. You will also need to install additional Python
packages needed by the workbooks, and a few additional programs.

The easiest way to get this all working is to install the free Anaconda
Python distribution provided by Continuum Analytics
(<https://www.continuum.io/downloads>). Anaconda includes a Jupyter
server and precompiled versions of many packages used in the workbooks.
It includes multiple tools for installing and updating both Python and
installed packages. It is separate from any OS-level version of Python,
and is easy to completely uninstall.

Anaconda also works on Windows as it does on Mac and Linux. Windows is a
much different operating system from Apple's OS X and Unix/Linux, and
Python has historically been much trickier to install, configure, and
use on Windows. Packages are harder to compile and install, the
environment can be more difficult to set up, etc. Anaconda makes Python
easier to work with on any OS, and on Windows, in a single run of the
Anaconda installer, it integrates Python and common Python utilities
like `pip` into Windows well enough that it approximates the ease and
experience of using Python within OS X or Unix/Linux (no small feat).

You can also create your Python environment manually, installing Python,
package managers, and Python packages separately. Packages like `numpy` and `pandas` can
be difficult to get working, however, particularly on Windows, and
Anaconda simplifies this setup considerably regardless of your OS.

### Central workbook server

Setting up a server to host workbooks managed by `nbgrader` is more involved. Some
of the workbooks consume multiple gigabytes of memory per user and
substantial processing power. A hosted implementation where all users
work on a single server requires substantial hardware, relatively
complex configuration, and ongoing server maintenance. Detailed
instructions are included in the Big-Data-Workbooks GitHub repository.
It is not rocket science, but it is complicated, and you will likely
need an IT professional to help you set up, maintain, and troubleshoot.
Since all student work will be centralized in this one location, you
will also want a robust, multi-destination backup plan.

For more information on installing and running the workbooks that
accompany this book, see the Big-Data-Workbooks GitHub repository.

Workbook details
----------------

Most chapters have an associated workbook, each in its own directory in
the Big-Data-Workbooks GitHub repository. Below is a list of the
workbooks, along with a short summary of the topics that each covers.

### Social Media and APIs

The Social Media and APIs workbook introduces you to the use of
Internet-based web service APIs for retrieving data from online data
stores. Examples include retrieving information on articles from
Crossref (provider of Digital Object Identifiers used as unique IDs for
publications) and using the PLOS Search and ALM APIs to retrieve
information on how articles are shared and referenced in social media,
focusing on Twitter. In this workbook, you will learn how to:

-   Set up user API keys,

-   Connect to Internet-based data stores using APIs,

-   Collect DOIs and Article-Level Metrics data from web APIs,

-   Conduct basic analysis of publication data.

### Database basics

In the Database workbook you will learn the practical benefits that stem
from using a database management system. You will implement basic SQL
commands to query grants, patents, and vendor data, and thus learn how
to interact with data stored in a relational database. You will also be
introduced to using Python to execute and interact with the results of
SQL queries, so you can write programs that interact with data stored in
a database. In this workbook, you will learn how to:

-   Connect to a database through Python,

-   Query the database by using SQL in Python,

-   Begin to understand to the SQL query language,

-   Close database connections.

### Data Linkage

In the Data Linkage workbook you will use Python to clean input data,
including using regular expressions, then learn and implement the basic
concepts behind the probabilistic record linkage: using different types
of string comparators to compare multiple pieces of information between
two records to produce a score that indicates how likely it is that the
records are data about the same underlying entity. In this workbook, you
will learn how to:

-   Parse a name string into first, middle, and last names using
    Python's `split` method and regular expressions,

-   Use and evaluate the results of common computationalstring
    comparison algorithms including Levenshtein
    distance,Levenshtein--Damerau distance, and Jaro--Winkler distance,

-   Understand the Fellegi--Sunter probabilistic record linkagemethod,
    with step-by-step implementation guide.

### Machine Learning

In the Machine Learning workbook you will train a machine learning model
to predict missing information, working through the process of cleaning
and prepping data for training and testing a model, then training and
testing a model to impute values for a missing categorical variable,
predicting the academic department of a given grant's primary
investigator based on other traits of the grant. In this workbook, you
will learn how to:

-   Read, clean, filter, and store data with Python's `pandas` data analysis
    package,

-   Recognize the types of data cleaning and refining needed to make
    data more compatible with machine learning models,

-   Clean and refine data,

-   Manage memory when working with large data sets,

-   Employ strategies for dividing data to properly train and test a
    machine learning model,

-   Use the `scikit-learn` Python package to train, fit, and evaluate machine learning
    models.

### Text Analysis

In the Text Analysis workbook, you will derive a list of topics from
text documents using MALLET, a Java-based tool that analyzes clusters of
words across a set of documents to derive common topics within the
documents, defined by sets of key words that are consistently used
together. In this workbook, you will learn how to:

-   Clean and prepare data for automated text analysis,

-   Set up data for use in MALLET,

-   Derive a set of topics from a collection of text documents,

-   Create a model that detects these topics in documents, and use this
    model to categorize documents.

### Networks

In the Networks workbook you will create network data where the nodes
are researchers who have been awarded grants, and ties are created
between each researcher on a given grant. You will use Python to read
the grant data and translate them into network data, then use the `networkx` Python
library to calculate node- and graph-level network statistics and `igraph` to
create and refine network visualizations. You will also be introduced to
graph databases, an alternative way of storing and querying network
data. In this workbook, you will learn how to:

-   Develop strategies for detecting potential network data in
    relational data sets,

-   Use Python to derive network data from a relational database,

-   Store and query network data using a graph database like `neo4j`,

-   Load network data into `networkx`, then use it to calculate node- and
    graph-level network statistics,

-   Use `networkx` to export graph data into commonly shared formats (`graphml`, edge lists,
    different tabular formats, etc.),

-   Load network data into the `igraph` Python package and then create graph
    visualizations.

### Visualization

The Visualization workbook introduces you to Tableau, a data analysis
and visualization software package that is easy to learn and use.
Tableau allows you to connect to and integrate multiple data sources
into complex visualizations without writing code. It allows you to
dynamically shift between views of data to build anything from single
visualizations to an interactive dashboard that contains multiple views
of your data. In this workbook, you will learn how to:

-   Connect Tableau to a relational database,

-   Interact with Tableau's interface,

-   Select, combine, and filter the tables and columns included in
    visualizations,

-   Create bar charts, timeline graphs, and heat maps,

-   Group and aggregate data,

-   Create a dashboard that combines multiple views of your data.

Resources
---------

We noted in
Section [Introduction: Resources](#sec:intro:resources) the importance of Python, MySQL, and
Git/GitHub for the social scientist who intends to work with large data.
See that section for pointers to useful online resources, and also this
book's website, at <https://github.com/BigDataSocialScience>, where we
have collected many useful web links, including the following.

For more on getting started with Anaconda, see Continuum's Anaconda
documentation [@Anaconda], Anaconda FAQ [@AnacondaFAQ], and Anaconda
quick start guide [@AnacondaQSG].

For more information on IPython and the Jupyter notebook server, see the
IPython site [@ipython], IPython documentation [@ipythondoc], Jupyter
Project site [@juypter], and Jupyter Project documentation
[@juypterdoc].

For more information on using `jupyterhub` and `nbgrader` to host, distribute, and grade
workbooks using a central server, see the `jupyterhub` GitHub repository
[@juypterhub], `jupyterhub` documentation [@juypterhubdoc], `nbgrader` GitHub repository
[@nbgrader], `nbgrader` and documentation [@nbgraderdoc].
