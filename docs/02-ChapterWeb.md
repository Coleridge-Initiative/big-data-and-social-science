Working with Web Data and APIs {#chap:web}
==============================

\chapterauthor{Cameron Neylon}
This chapter will show you how to extract information from social media
about the transmission of knowledge. The particular application will be
to develop links to authors' articles on Twitter using PLOS articles and
to pull information using an API. You will get link data from
bookmarking services, citations from Crossref, links from Facebook, and
information from news coverage. The examples that will be used are from
Twitter. In keeping with the social science grounding that is a core
feature of the book, it will discuss what can be captured, what is
potentially reliable, and how to manage data quality issues.

Introduction
------------

A tremendous lure of the Internet is the availability of vast amounts of
data on businesses, people, and their activity on social media. But how
can we capture the information and make use of it as we might make use
of more traditional data sources? In this chapter, we begin by
describing how web data can be collected, using the use case of UMETRICS
and research output as a readily available example, and then discuss how
to think about the scope, coverage, and integration issues associated
with its collection.

Often a big data exploration starts with information on people or on a
group of people. The web can be a rich source of additional information.
It can also act as pointers to new sources of information, allowing a
pivot from one perspective to another, from one kind of query to
another. Often this is exploratory. You have an existing core set of
data and are looking to augment it. But equally this exploration can
open up whole new avenues. Sometimes the data are completely
unstructured, existing as web pages spread across a site, and sometimes
they are provided in a machine-readable form. The challenge is in having
a sufficiently diverse toolkit to bring all of this information
together.

Using the example of data on researchers and research outputs, we will
explore obtaining information directly from web pages (*web scraping*)
as well as explore the uses of APIs--- web services that allow an
interaction with, and retrieval of, structured data. You will see how
the crucial pieces of integration often lie in making connections
between disparate data sets and how in turn making those connections
requires careful quality control. The emphasis throughout this chapter
is on the importance of focusing on the purpose for which the data will
be used as a guide for data collection. While much of this is specific
to data about research and researchers, the ideas are generalizable to
wider issues of data and public policy.

Scraping information from the web {#sec:4-1}
---------------------------------

With the range of information available on the web, our first question
is how to access it. The simplest approach is often to manually go
directly to the web and look for data files or other information. For
instance, on the NSF website [@nsfweb] it is possible to obtain data
dumps of all grant information. Sometimes data are available only on web
pages or we only want a subset of this information. In this case web
scraping is often a viable approach.

Web scraping involves using a program to download and process web pages
directly. This can be highly effective, particularly where tables of
information are made available online. It is also useful in cases where
it is desirable to make a series of very similar queries. In each case
we need to look at the website, identify how to get the information we
want, and then process it. Many websites deliberately make this
difficult to prevent easy access to their underlying data.

### Obtaining data from the HHMI website {#sec:4-1.1}

Let us suppose we are interested in obtaining information on those
investigators that are funded by the Howard Hughes Medical Institute
(HHMI). HHMI has a website that includes a search function for funded
researchers, including the ability to filter by field, state, and role.
But there does not appear to be a downloadable data set of this
information. However, we can automate the process with code to create a
data set that you might compare with other data.

This process involves first understanding how to construct a URL that
will do the search we want. This is most easily done by playing with
search functionality and investigating the URL structures that are
returned. Note that in many cases websites are not helpful here.
However, with HHMI if we do a general search and play with the structure
of the URL, we can see some of the elements of the URL that we can think
of as a query. As we want to see *all* investigators, we do not need to
limit the search, and so with some fiddling we come up with a URL like
the following. (We have broken the one-line URL into three lines for
ease of presentation.)

\enlargethispage{6pt}

http://www.hhmi.org/scientists/browse?
kw=&sort_by=field_scientist_last_name&
sort_order=ASC&items_per_page=20&page=0

The `requests` module, available natively in Jupyter Python notebooks, is a useful
set of tools for handling interactions with websites. It lets us
construct the request that we just presented in terms of a base URL and
query terms, as follows:


```r
>> BASE_URL = "http://www.hhmi.org/scientists/browse"
>> query = {
            "kw" : "",
            "sort_by" : "field_scientist_last_name",
            "sort_order" : "ASC",
            "items_per_page" : 20,
            "page" : None
           }
```

With our request constructed we can then make the call to the web page
to get a response.


```r
>> import requests
>> response = requests.get(BASE_URL, params=query)
```

The first thing to do when building a script that hits a web page is to
make sure that your call was successful. This can be checked by looking
at the response code that the web server sent---and, obviously, by
checking the actual HTML that was returned. A `200` code means success and
that everything should be OK. Other codes may mean that the URL was
constructed wrongly or that there was a server error.


```r
>> response.status_code
200
```

With the page successfully returned, we now need to process the text it
contains into the data we want. This is not a trivial exercise. It is
possible to search through and find things, but there are a range of
tools that can help with processing HTML and XML data. Among these one
of the most popular is a module called BeautifulSoup [@bsoup], which
provides a number of useful functions for this kind of processing. The
module documentation provides more details.

We need to check the details of the page source to find where the
information we are looking for is kept (see, for example,
\@ref(fig:fig2-1)). Here, all the details on HHMI investigators can
be found in a `<div>` element with the class attribute `view-content`. This structure is not
something that can be determined in advance. It requires knowledge of
the structure of the page itself. Nested inside this `<div>` element are another
series of `div`s, each of which corresponds to one investigator. These have
the class attribute `view-rows`. Again, there is nothing obvious about finding
these, it requires a close examination of the page HTML itself for any
specific case you happen to be looking at.

<div class="figure" style="text-align: center">
<img src="ChapterWeb/figures/fig2-1.png" alt="Source HTML from the portion of an HHMI results page containing information on HHMI investigators; note that the webscraping results in badly formatted html which is difficult to read." width="70%" />
<p class="caption">(\#fig:fig2-1)Source HTML from the portion of an HHMI results page containing information on HHMI investigators; note that the webscraping results in badly formatted html which is difficult to read.</p>
</div>

\vspace*{-8pt}
We first process the page using the BeautifulSoup module (into the
variable `soup`) and then find the `div` element that holds the information on
investigators (`investigator_list`). As this element is unique on the page (I checked using
my web browser), we can use the find method. We then process that `div` (using
`find_all`) to create an iterator object that contains each of the page segments
detailing a single investigator (`investigators`).


```r
>> from bs4 import BeautifulSoup
>> soup = BeautifulSoup(response.text, "html5lib")
>> investigator_list = soup.find('div', class_ = "view-content")
>> investigators = investigator_list.find_all("div", class_ = "views-row")
```

\enlargethispage{24pt}
As we specified in our query parameters that we wanted 20 results per
page, we should check whether our list of page sections has the right
length.


```r
>> len(investigators)
20
```

\enlargethispage{12pt}

```r
# Given a request response object, parse for HHMI investigators
def scrape(page_response):
   # Obtain response HTML and the correct <div> from the page
   soup = BeautifulSoup(response.text, "html5lib")
   inv_list = soup.find('div', class_ = "view-content")

   # Create a list of all the investigators on the page
   investigators = inv_list.find_all("div", class_ = "views-row")

   data = [] # Make the data object to store scraping results

   # Scrape needed elements from investigator list
   for investigator in investigators:
       inv = {} # Create a dictionary to store results

       # Name and role are in same HTML element; this code
       # separates them into two data elements
       name_role_tag = investigator.find("div",
           class_ = "views-field-field-scientist-classification")
       strings = name_role_tag.stripped_strings
       for string,a in zip(strings, ["name", "role"]):
           inv[a] = string

       # Extract other elements from text of specific divs or from
       # class attributes of tags in the page (e.g., URLs)
       research_tag = investigator.find("div",
          class_ = "views-field-field-scientist-research-abs-nod")
       inv["research"] = research_tag.text.lstrip()
       inv["research_url"] = "http://hhmi.org"
          + research_tag.find("a").get("href")
       institution_tag = investigator.find("div",
          class_ = "views-field-field-scientist-academic-institu")
       inv["institute"] = institution_tag.text.lstrip()
       town_state_tag = investigator.find("div",
           class_ = "views-field-field-scientist-institutionstate")
       inv["town"], inv["state"] = town_state_tag.text.split(",")
       inv["town"] = inv.get("town").lstrip()
       inv["state"] = inv.get("state").lstrip()

       thumbnail_tag = investigator.find("div",
          class_ = "views-field-field-scientist-image-thumbnail")
       inv["thumbnail_url"] = thumbnail_tag.find("img")["src"]
       inv["url"] = "http://hhmi.org"
          + thumbnail_tag.find("a").get("href")

       # Add the new data to the list
       data.append(inv)
   return data
```

\pagebreak
Finally, we need to process each of these segments to obtain the data we
are looking for. This is the actual "scraping" of the page to get the
information we want. Again, this involves looking closely at the HTML
itself, identifying where the information is held, what tags can be used
to find it, and often doing some postprocessing to clean it up (removing
spaces, splitting different elements up).

Listing \@ref(fig:web-py1) provides a function to handle all of this. The
function accepts the response object from the requests module as its
input, processes the page text to soup, and then finds the `investigator_list` as above and
processes it into an actual list of the investigators. For each
investigator it then processes the HTML to find and clean up the
information required, converting it to a dictionary and adding it to our
growing list of data.

Let us check what the first two elements of our data set now look like.
You can see two dictionaries, one relating to Laurence Abbott, who is a
senior fellow at the HHMI Janelia Farm Campus, and one for Susan
Ackerman, an HHMI investigator based at the Jackson Laboratory in Bar
Harbor, Maine. Note that we have also obtained URLs that give more
details on the researcher and their research program (`research_url` and `url` keys in the
dictionary) that could provide a useful input to textual analysis or
topic modeling (see
[Text Analysis](#chap:text)).


```r
>> data = scrape(response)
>> data[0:2]
[{'institute': u'Janelia Research Campus ',
  'name': u'Laurence Abbott, PhD',
  'research': u'Computational and Mathematical Modeling of Neurons and Neural... ',
  'research_url': u'http://hhmi.org/research/computational-and-mathematical-modeling-neurons-and-neural-networks',
  'role': u'Janelia Senior Fellow',
  'state': u'VA ',
  'thumbnail_url': u'http://www.hhmi.org/sites/default/files/Our%20Scientists/Janelia/Abbott-112x112.jpg',
  'town': u'Ashburn',
  'url': u'http://hhmi.org/scientists/laurence-f-abbott'},
 {'institute': u'The Jackson Laboratory ',
  'name': u'Susan Ackerman, PhD',
  'research': u'Identification of the Molecular Mechanisms Underlying... ',
  'research_url': u'http://hhmi.org/research/identification-molecular-mechanisms-underlying-neurodegeneration',
  'role': u'Investigator',
  'state': u'ME ',
  'thumbnail_url':
u'http://www.hhmi.org/sites/default/files/Our%20Scientists/Investigators/Ackerman-112x112.jpg',
  'town': u'Bar Harbor',
  'url': u'http://hhmi.org/scientists/susan-l-ackerman'}]
```

So now we know we can process a page from a website to generate usefully
structured data. However, this was only the first page of results. We
need to do this for each page of results if we want to capture all the
HHMI investigators. We could just look at the number of pages that our
search returned manually, but to make this more general we can actually
scrape the page to find that piece of information and use that to
calculate how many pages we need to work through.

The number of results is found in a `div` with the class "view-headers" as a
piece of free text ("Showing 1--20 of 493 results"). We need to grab the
text, split it up (I do so based on spaces), find the right number (the
one that is before the word "results") and convert that to an integer.
Then we can divide by the number of items we requested per page (20 in
our case) to find how many pages we need to work through. A quick mental
calculation confirms that if page 0 had results 1--20, page 24 would
give results 481--493.


```r
>> # Check total number of investigators returned
>> view_header = soup.find("div", class_ = "view-header")
>> words = view_header.text.split(" ")
>> count_index = words.index("results.") - 1
>> count = int(words[count_index])

>> # Calculate number of pages, given count & items_per_page
>> num_pages = count/query.get("items_per_page")
>> num_pages
24
```

Then it is a simple matter of putting the function we constructed
earlier into a loop to work through the correct number of pages. As we
start to hit the website repeatedly, we need to consider whether we are
being polite. Most websites have a file in the root directory called
robots.txt that contains guidance on using programs to interact with the
website. In the case of <http://hhmi.org> the file states first that we
are allowed (or, more properly, not forbidden) to query
<http://www.hhmi.org/scientists/> programmatically. Thus, you can pull
down all of the more detailed biographical or research information, if
you so desire. The file also states that there is a requested
"Crawl-delay" of 10. This means that if you are making repeated queries
(as we will be in getting the 24 pages), you should wait for 10 seconds
between each query. This request is easily accommodated by adding a
timed delay between each page request.

\pagebreak

```r
>> for page_num in range(num_pages):
>> # We already have page zero and we need to go to 24:
>> # range(24) is [0,1,...,23]
>>    query["items_per_page"] = page_num + 1
>>    page = requests.get(BASE_URL, params=query)
>> # We use extend to add list for each page to existing list
>>    data.extend(scrape(page))
>> print "Retrieved and scraped page number:", query.get("items_per_page")
>> time.sleep(10) # robots.txt at hhmi.org specifies a crawl delay of 10 seconds
Retrieved and scraped page number: 1
Retrieved and scraped page number: 2
...
Retrieved and scraped page number: 24
```

Finally we can check that we have the right number of results after our
scraping. This should correspond to the 493 records that the website
reports.


```r
>> len(data)
493
```

### Limits of scraping {#sec:4-1.2}

While scraping websites is often necessary, is can be a fragile and
messy way of working. It is problematic for a number of reasons: for
example, many websites are designed in ways that make scraping difficult
or impossible, and other sites explicitly prohibit this kind of scripted
analysis. (Both reasons apply in the case of the NSF and Grants.gov
websites, which is why we use the HHMI website in our example.)

In many cases a better choice is to process a data dump from an
organization. For example, the NSF and Wellcome Trust both provide data
sets for each year that include structured data on all their awarded
grants. In practice, integrating data is a continual challenge of
figuring out what is the easiest way to proceed, what is allowed, and
what is practical and useful. The selection of data will often be driven
by pragmatic rather than theoretical concerns.

Increasingly, however, good practice is emerging in which organizations
provide APIs to enable scripted and programmatic access to the data they
hold. These tools are much easier and generally more effective to work
with. They are the focus of much of the rest of this chapter.

New data in the research enterprise {#sec:4-2}
-----------------------------------

The new forms of data we are discussing in this chapter are largely
available because so many human activities---in this case, discussion,
reading, and bookmarking---are happening online. All sorts of data are
generated as a side effect of these activities. Some of that data is
public (social media conversations), some private (IP addresses
requesting specific pages), and some intrinsic to the service (the
identity of a user who bookmarks an article). What exactly are these new
forms of data? There are broadly two new directions that data
availability is moving in. The first is information on new forms of
research output, data sets, software, and in some cases physical
resources. There is an interest across the research community in
expanding the set of research outputs that are made available and, to
drive this, significant efforts are being made to ensure that these
nontraditional outputs are seen as legitimate outputs. In particular
there has been a substantial policy emphasis on data sharing and,
coupled with this, efforts to standardize practice around data citation.
This is applying a well-established measure (citation) to a new form of
research output.

The second new direction, which is more developed, takes the alternate
route, providing *new forms of information on existing types of output*,
specifically research articles. The move online of research activities,
including discovery, reading, writing, and bookmarking, means that many
of these activities leave a digital trace. Often these traces are public
or semi-public and can be collected and tracked. This certainly raises
privacy issues that have not been comprehensively addressed but also
provides a rich source of data on who is doing what with research
articles.

<div class="figure" style="text-align: center">
<img src="ChapterWeb/figures/fig2-2.png" alt="Classes of online activity related to research journal articles. Reproduced from Lin and Fenner [237], under a Creative Commons Attribution v 3.0 license" width="70%" />
<p class="caption">(\#fig:fig2-2)Classes of online activity related to research journal articles. Reproduced from Lin and Fenner [237], under a Creative Commons Attribution v 3.0 license</p>
</div>

There are a wide range of potential data sources, so it is useful to
categorize them. Figure \@ref(fig:fig2-2) shows one possible categorization, in which data
sources are grouped based on the level of engagement and the stage of
use. It starts from the left with "views," measures of online views and
article downloads, followed by "saves" where readers actively collect
articles into a library of their own, through online *discussion* forums
such as blogs, social media and new commentary, formal scholarly
*recommendations*, and, finally, formal *citations*.

These categories are a useful way to understand the classes of
information available and to start digging into the sources they can be
obtained from. For each category we will look at the *kind* of usage
that the indicator is a proxy for, which *users* are captured by the
indicator, the *limitations* that the indicator has as a measure, and
the *sources* of data. We start with the familiar case of formal
literature citations to provide context.

---

**Example: Citations**

Most quantitative analyses of research have focused on citations from
research articles to other research articles. Many familiar
measures---such as Impact Factors, Scimago Journal Rank, or
Eigenfactor---are actually measures of journal rather than article
performance. However, information on citations at the article level is
increasingly the basis for much bibliometric analysis.

-   Kind of usage

    -   Citing a scholarly work is a signal from a researcher that a
        specific work has relevance to, or has influenced, the work they
        are describing.

    -   It implies significant engagement and is a measure that carries
        some weight.

-   Users

    -   Researchers, which means usage by a specific group for a fairly
        small range of purposes.

    -   With high-quality data, there are some geographical, career, and
        disciplinary demographic details.

-   Limitations

    -   The citations are slow to accumulate, as they must pass through
        a peer-review process.

    -   It is seldom clear from raw data why a paper is being cited.

    -   It provides a limited view of usage, as it only reflects reuse
        in research, not application in the community.

-   Sources

    -   Public sources of citation data include PubMed Central and
        Europe PubMed Central, which mine publicly available full text
        to find citations.

    -   Proprietary sources of citation data include Thomson Reuters'
        Web of Knowledge and Elsevier's Scopus.

    -   Some publishers make citation data collected by Crossref
        available.
        
---

---

**Example: Page views and downloads**

A major new source of data online is the number of times articles are
viewed. Page views and downloads can be defined in different ways and
can be reached via a range of paths. Page views are an immediate measure
of usage. Viewing a paper may involve less engagement than citation or
bookmarking, but it can capture interactions with a much wider range of
users.

The possibility of drawing demographic information from downloads has
significant potential for the future in providing detailed information
on who is reading an article, which may be valuable for determining, for
example, whether research is reaching a target audience.

-   Kind of usage

    -   It counts the number of people who have clicked on an article
        page or downloaded an article.

-   Users

    -   Page views and downloads report on use by those who have access
        to articles. For publicly accessible articles this could be
        anyone; for subscription articles it is likely to be
        researchers.

-   Limitations

    -   Page views are calculated in different ways and are not directly
        comparable across publishers. Standards are being developed but
        are not yet widely applied.

    -   Counts of page views cannot easily distinguish between
        short-term visitors and those who engage more deeply with an
        article.

    -   There are complications if an article appears in multiple
        places, for example at the journal website and a repository.

    \pagebreak
-   Sources

    -   Some publishers and many data repositories make page view data
        available in some form. Publishers with public data include
        PLOS, Nature Publishing Group, Ubiquity Press, Co-Action Press,
        and Frontiers.

    -   Data repositories, including Figshare and Dryad, provide page
        view and download information.

    -   PubMed Central makes page views of articles hosted on that site
        available to depositing publishers. PLOS and a few other
        publishers make this available.
        
---

---

**Example: Analyzing bookmarks** 

Tools for collecting and curating personal collections of literature, or
web content, are now available online. They make it easy to make copies
and build up indexes of articles. Bookmarking services can choose to
provide information on the number of people who have bookmarked a paper.

Two important services targeted at researchers are Mendeley and
CiteULike. Mendeley has the larger user base and provides richer
statistics. Data include the number of users that who bookmarked a
paper, groups that have collected a paper, and in some cases
demographics of users, which can include discipline, career stage, and
geography.

Bookmarks accumulate rapidly after publication and provide evidence of
scholarly interest. They correlate quite well with the eventual number
of citations. There are also public bookmarking services that provide a
view onto wider interest in research articles.

-   Kind of usage

    -   Bookmarking is a purposeful act. It may reveal more interest
        than a page view, but less than a citation.

    -   Its uses are different from those captured by citations.

    -   The bookmarks may include a variety of documents, such as papers
        for background reading, introductory material, position or
        policy papers, or statements of community positions.

-   Users

    -   Academic-focused services provide information on use by
        researchers.

    -   Each service has a different user profile in, for instance,
        sciences or social sciences.

    -   All services have a geographical bias towards North America and
        Europe.

    -   There is some demographic information, for instance, on
        countries where users are bookmarking the most.

-   Limitations

    -   There is bias in coverage of services; for instance, Mendeley
        has good coverage of biomedical literature.

    -   It can only report on activities of signed-up users.

    -   It is not usually possible to determine why a bookmark has been
        created.

-   Sources

    -   Mendeley and CiteULike both have public APIs that provide data
        that are freely available for reuse.

    -   Most consumer bookmarking services provide some form of API, but
        this often has restrictions or limitations.

---

---

**Example: Discussions on social media**

Social media are one of the most valuable new services producing
information about research usage. A growing number of researchers,
policymakers, and technologists are on these services discussing
research.

There are three major features of social media as a tool. First, among a
large set of conversations, it is possible to discover a discussion
about a specific paper. Second, Twitter makes it possible to identify
groups discussing research and to learn whether they were potential
targets of the research. Third, it is possible to reconstruct
discussions to understand what paths research takes to users.

In the future it will be possible to identify target audiences and to
ask whether they are being reached and how modified distribution might
maximize that reach. This could be a powerful tool, particularly for
research with social relevance.

Twitter provides the most useful data because discussions and the
identity of those involved are public. Connections between users and the
things they say are often available, making it possible to identify
communities discussing work. However, the 140-character limit on Twitter
messages ("tweets") does not support extended critiques. Facebook has
much less publicly available information--- but being more private, it
can be a site for frank discussion of research.

-   Kind of usage

    -   Those discussing research are showing interest potentially
        greater than page views.

    -   Often users are simply passing on a link or recommending an
        article.

    -   It is possible to navigate to tweets and determine the level and
        nature of interest.

    -   Conversations range from highly technical to trivial, so numbers
        should be treated with caution.

    -   Highly tweeted or Facebooked papers also tend to have
        significant bookmarking and citation.

    -   Professional discussions can be swamped when a piece of research
        captures public interest.

-   Users

    -   The user bases and data sources for Twitter and Facebook are
        global and public.

    -   There are strong geographical biases.

    -   A rising proportion of researchers use Twitter and Facebook for
        professional activities.

    -   Many journalists, policymakers, public servants, civil society
        groups, and others use social media.

-   Limitations

    -   Frequent lack of explicit links to papers is a serious
        limitation.

    -   Use of links is biased towards researchers and against groups
        not directly engaged in research.

    -   There are demographic issues and reinforcement
        effects---retweeting leads to more retweeting in preference to
        other research---so analysis of numbers of tweets or likes is
        not always useful.

\---

---

**Example: Recommendations**

A somewhat separate form of usage is direct expert recommendations. The
best-known case of this is the F1000 service on which experts offer
recommendations with reviews of specific research articles. Other
services such as collections or personal recommendation services may be
relevant here as well.

-   Kind of usage

    -   Recommendations from specific experts show that particular
        outputs are worth looking at in detail, are important, or have
        some other value.

    -   Presumably, recommendations are a result of in-depth reading and
        a high level of engagement.

    \pagebreak
-   Users

    -   Recommendations are from a selected population of experts
        depending on the service in question.

    -   In some cases this might be an algorithmic recommendation
        service.

-   Limitations

    -   Recommendations are limited to the interests of the selected
        population of experts.

    -   The recommendation system may be biased in terms of the
        interests of recommenders (e.g., towards---or away from---new
        theories vs. developing methodology) as well as their
        disciplines.

    -   Recommendations are slow to build up.

---

A functional view {#sec:4-3}
-----------------

The descriptive view of data types and sources is a good place to start,
but it is subject to change. Sources of data come and go, and even the
classes of data types may expand and contract in the medium to long
term. We also need a more functional perspective to help us understand
how these sources of data relate to activities in the broader research
enterprise.

Consider Figure \@ref(fig:fig2) in
Chapter [Introduction](#chap:intro). The research enterprise has been framed as
being made up of people who are generating outputs. The data that we
consider in this chapter relate to connections between outputs, such as
citations between research articles and tweets referring to articles.
These connections are themselves created by people, as shown in Figure
\@ref(fig:fig2-3). The people in
turn may be classed as belonging to certain categories or communities.
What is interesting, and expands on the simplified picture of
Figure \@ref(fig:fig2), is that many of these people are not
professional researchers. Indeed, in some cases they may not be people
at all but automated systems of some kind. This means we need to expand
the set of actors we are considering. As described above, we are also
expanding the range of outputs (or objects) that we are considering as
well.

<div class="figure" style="text-align: center">
<img src="ChapterWeb/figures/fig2-3.png" alt="A simplified model of online interactions between research outputs and the objects that refer to them" width="70%" />
<p class="caption">(\#fig:fig2-3)A simplified model of online interactions between research outputs and the objects that refer to them</p>
</div>

In the simple model of Figure \@ref(fig:fig2-3), there are three categories of things (nodes on the
graph): objects, people, and the communities they belong to. Then there
are the relationships between these elements (connections between
nodes). Any given data source may provide information on different parts
of this graph, and the information available is rarely complete or
comprehensive. Data from different sources can also be difficult to
integrate. As with any data integration, combining sources relies on
being able to confidently identify those nodes that are common between
data sources. Therefore identifying unique objects and people is
critical to making progress.

These data are not necessarily public but many services choose to make
some data available. An important characteristic of these data sources
is that they are completely in the gift of the service provider. Data
availability, its presentation, and upstream analysis can change without
notice. Data are sometimes provided as a dump but is also frequently
provided through an API.

An API is simply a tool that allows a program to interface with a
service. APIs can take many different forms and be of varying quality
and usefulness. In this section we will focus on one common type of API
and examples of important publicly available APIs relevant to research
communications. We will also cover combining APIs and the benefits and
challenges of bringing multiple data sources together.

### Relevant APIs and resources {#sec:4-3.1}

There is a wide range of other sources of information that can be used
in combination with the APIs featured above to develop an overview of
research outputs and of where and how they are being used. There are
also other tools that can allow deeper analysis of the outputs
themselves.
Table [\[tab:chapAPI:1\]](#tab:chapAPI:1){reference-type="ref"
reference="tab:chapAPI:1"} gives a partial list of key data sources and
APIs that are relevant to the analysis of research outputs.

\small
  **Source**                  **Description**                                                                                                                                                                                                 **API**   **Free**
  --------------------------- -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- --------- ----------
                                                                                                                                                                                                                                                       
  PubMed                      An online index that combines bibliographic data from Medline and PubMed Central. PubMed Central and Europe PubMed Central also provide information.                                                               Y         Y
  Web of Science              The bibliographic database provided by Thomson Reuters. The ISI Citation Index is also available.                                                                                                                  Y         N
  Scopus                      The bibliographic database provided by Elsevier. It also provides citation information.                                                                                                                            Y         N
  Crossref                    Provides a range of bibliographic metadata and information obtained from members registering DOIs.                                                                                                                 Y         Y
  Google Scholar              Provides a search index for scholarly objects and aggregates citation information.                                                                                                                                 N         Y
  Microsoft Academic Search   Provides a search index for scholarly objects and aggregates citation information. Not as complete as Google Scholar, but has an API.                                                                              Y         Y
                                                                                                                                                                                                                                                       
  Altmetric.com               A provider of aggregated data on social media and mainstream media attention of research outputs. Most comprehensive source of information across different social media and mainstream media conversations.       Y         N
  Twitter                     Provides an API that allows a user to search for recent tweets and obtain some information on specific accounts.                                                                                                   Y         Y
  Facebook                    The Facebook API gives information on the number of pages, likes, and posts associated with specific web pages.                                                                                                    Y         Y
                                                                                                                                                                                                                                                       
  ORCID                       Unique identifiers for research authors. Profiles include information on publication lists, grants, and affiliations.                                                                                              Y         Y
  LinkedIn                    CV-based profiles, projects, and publications.                                                                                                                                                                     Y         \*
                                                                                                                                                                                                                                                       
  Gateway to Research         A database of funding decisions and related outputs from Research Councils UK.                                                                                                                                     Y         Y
  NIH Reporter                Online search for information on National Institutes of Health grants. Does not provide an API but a downloadable data set is available.                                                                           N         Y
  NSF Award Search            Online search for information on NSF grants. Does not provide an API but downloadable data sets by year are available.                                                                                             N         Y

The data are restricted: sometimes fee based, other times not.

### RESTful APIs, returned data, and Python wrappers {#sec:4-3.2}

The APIs we will focus on here are all examples of RESTful services.
REST stands for Representational State Transfer
[@RESTwiki; @fielding2002principled], but for our purposes it is most
easily understood as a means of transferring data using web protocols.
Other forms of API require additional tools or systems to work with, but
RESTful APIs work directly over the web. This has the advantage that a
human user can also with relative ease play with the API to understand
how it works. Indeed, some websites work simply by formatting the
results ofAPI calls.

As an example let us look at the Crossref API. This provides a range of
information associated with Digital Object Identifiers (DOIs) registered
with Crossref. DOIs uniquely identify an object, and Crossref DOIs refer
to research objects, primarily (but not entirely) research articles. If
you use a web browser to navigate to
<http://api.crossref.org/works/10.1093/nar/gni170>, you should receive
back a webpage that looks something like the following. (We have laid it
out nicely to make it more readable.)


```r
{ "status" : "ok",
  "message-type" : "work",
  "message-version" : "1.0.0",
  "message" :
   { "subtitle": [],
     "subject" : ["Genetics"],
     "issued" : { "date-parts" : [[2005,10,24]] },
     "score" : 1.0,
     "prefix" : "http://id.crossref.org/prefix/10.1093",
     "author" : [ "affiliation" : [],
                   "family" : "Whiteford",
                   "given" : "N."}],
     "container-title" : ["Nucleic Acids Research"],
     "reference-count" : 0,
     "page" : "e171-e171",
     "deposited" : {"date-parts" : [[2013,8,8]],
                    "timestamp" : 1375920000000},
     "issue" : "19",
     "title" :
       ["An analysis of the feasibility of short read sequencing"],
     "type" : "journal-article",
     "DOI" : "10.1093/nar/gni170",
     "ISSN" : ["0305-1048","1362-4962"],
     "URL" : "http://dx.doi.org/10.1093/nar/gni170",
     "source" : "Crossref",
     "publisher" : "Oxford University Press (OUP)",
     "indexed" : {"date-parts" : [[2015,6,8]],
                  "timestamp" : 1433777291246},
     "volume" : "33",
     "member" : "http://id.crossref.org/member/286"
   }
}
```

This is a package of JavaScript Object Notation (JSON) data returned in
response to a query. The query is contained entirely in the URL, which
can be broken up into pieces: the root URL (<http://api.crossref.org>)
and a data "query," in this case made up of a "field" (`works`) and an
identifier (the DOI `10.1093/nar/gni170`). The Crossref API provides information about the
article identified with this specific DOI.

Programming against an API {#sec:4-4}
--------------------------

Programming against an API involves constructing HTTP requests and
parsing the data that are returned. Here we use the Crossref API to
illustrate how this is done. Crossref is the provider of DOIs used by
many publishers to uniquely identify scholarly works. Crossref is not
the only organization to provide DOIs. The scholarly communication space
DataCite is another important provider. The documentation is available
at the Crossref website [@crossref].

Once again the `requests` Python library provides a series of convenience functions
that make it easier to make HTTP calls and to process returned JSON. Our
first step is to import the module and set a base URL variable.


```r
>> import requests
>> BASE_URL = "http://api.crossref.org/"
```

A simple example is to obtain metadata for an article associated with a
specific DOI. This is a straightforward call to the Crossref API,
similar to what we saw earlier.


```r
>> doi = "10.1093/nar/gni170"
>> query = "works/"
>> url = BASE_URL + query + doi
>> response = requests.get(url)
>> url
http://api.crossref.org/works/10.1093/nar/gni170
>> response.status_code
200
```

The `response` object that the `requests` library has created has a range of useful
information, including the URL called and the response code from the web
server (in this case 200, which means everything is OK). We need the
JSON body from the response object (which is currently text from the
perspective of our script) converted to a Python dictionary. The `requests` module
provides a convenient function for performing this conversion, as the
following code shows. (All strings in the output are in Unicode, hence
the "u
