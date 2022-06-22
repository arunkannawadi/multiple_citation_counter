from scholarly import scholarly, ProxyGenerator, MaxTriesExceededException


def main(scholar_id, scraper_api_key=None, max_paper_count=None):

    pg = ProxyGenerator()
    proxy_works = False
    if scraper_api_key is not None:
        proxy_works = pg.ScraperAPI(scraper_api_key)
        if proxy_works is True:
            yield "Using ScraperAPI!<br>"
        elif proxy_works is False:
            yield "ScraperAPI is not working!<br>"

    if proxy_works is False:
        yield "Looking for free proxies...<br>"
        pg.FreeProxies()
        yield "Using FreeProxy! (This will be very slow. Go get a coffee and come back ... ) <br>"

    scholarly.use_proxy(pg)

    yield "Making contact with Google Scholar<br>"
    scholar = scholarly.search_author_id(scholar_id)
    scholarly.fill(scholar, sections=['basics', 'publications'])
    scholar_name = scholar["name"]
    yield f"Hello {scholar_name} !<br>"

    if max_paper_count is None:
        max_paper_count = len(scholar["publications"])

    citations_dict = {}
    for n, pub in enumerate(scholar['publications']):
        if pub['num_citations'] == 0:
            break
        if n >= max_paper_count:
            break
        yield f"Fetching {pub['num_citations']} citation(s) of the article titled {pub['bib']['title']}<br>"
        key = pub['author_pub_id']
        citations_dict[key] = []
        for cites_id in pub.get('cites_id', []):
            try:
                citations_dict[key] += list(scholarly.search_citedby(int(cites_id)))
            except MaxTriesExceededException:
                return "Unable to fetch citations without a valid ScraperAPI key"

    reference_dict = {}
    for pub, citations in citations_dict.items():
      for citation in citations:
        try:
          key = citation['pub_url']
        except KeyError:
          key = citation['bib']['title']

        try:
          reference_dict[key].append(pub)
        except KeyError:
          reference_dict[key] = [pub]

    yield "Done!<br><hr><hr>"
    for reference, papers in reference_dict.items():
        if len(papers) > 1:
            yield f"<a href={reference}>{reference}</a> cites {len(papers)} papers<br>"
            for idx, paper in enumerate(papers):
                publication = [pub for pub in scholar['publications'] if pub['author_pub_id']==paper][0]
                yield f"{idx+1}. {publication['bib']['title']} ({publication.get('pub_url', 'No link found')})<br>"
            yield "<hr>"
