baomoi = {
    "published_date": ['/html/body/div/div[4]/div/div[1]/div[2]/div[2]/time/text()'],
    "source": ["/html/body/div/div[4]/div/div[1]/div[2]/p/a/span[2]/text()"],
    "title": ["/html/body/div/div[4]/div/div[1]/div[2]/h1/text()"],
    "summary": ["/html/body/div/div[4]/div/div[1]/div[2]/div[3]/text()"],
    "images": ["/html/body/div/div[4]/div/div[1]/div[2]/div[4]/p/img/@src"],
    "content": ["/html/body/div/div[4]/div/div[1]/div[2]/div[4]/p/descendant-or-self::*[not(self::script)]/text()"]
}
vnxexpress = {
    "published_date": ['/html/body/div/div[1]/article/div/span/text()', '//section[1]/header/span/text()'],
    "source": "empty",
    "title": ['/html/body/div/div[1]/article/h1/text()', '//section[1]/h1/text()'],
    "summary": "empty",
    "content": ['//section[1]/article/p/descendant-or-self::*[not(self::script)]/text()'],
    "images": ['//section[1]/article/table/tbody/tr[1]/td/img/@src', '//article/div/a/img/@src'],
}
dantri = {
    "published_date": ['/html/body/div[9]/div[3]/div/div[1]/div[1]/div[1]/div[1]/span/text()'],
    "source": "empty",
    "title": ['/html/body/div[9]/div[3]/div/div[1]/div[1]/div[1]/h1/text()'],
    "summary": "empty",
    "images": ["/html/body/div[9]/div[3]/div/div[1]/div[1]/div[1]/div[4]/div/figure/img/@src"],
    "content": ['/html/body/div[9]/div[3]/div/div[1]/div[1]/div[1]/div[4]/p/descendant-or-self::*[not(self::script)]/text()']
}
vietnamnet ={
    "published_date": ['//div[4]/div[1]/div[2]/div[4]/p[2]/text()'],
    "source": "empty",
    "title": ['//div[1]/div[2]/div[2]/h1/text()'],
    "summary": "empty",
    "content": ['//div[4]/div[1]/div[2]/div[1]/div[2]/div[1]/div/div/div[1]/a/descendant-or-self::*[not(self::script)]/text()'],
    "images": ["//div[2]/div[4]/table/tbody/tr[1]/td/img/@src"],
}