import logging

import wikipediaapi

logging.basicConfig(level=logging.INFO)

user_agent = "Wikipedia-API Example (merlin@example.com)"

wiki_wiki = wikipediaapi.Wikipedia(user_agent=user_agent, language="ru")

page_py = wiki_wiki.page("Кошки")

print("Page - Exists: %s" % page_py.exists())
print("Page - Id: %s" % page_py.pageid)
print("Page - Title: %s" % page_py.title)
print("Page - Summary: %s" % page_py.summary[0:60])


def print_sections(sections, level=0):
    for s in sections:
        print("{}: {} - {}".format("*" * (level + 1), s.title, s.text[0:40]))
        print_sections(s.sections, level + 1)


print("Sections:")
print_sections(page_py.sections)


def print_langlinks(page):
    langlinks = page.langlinks
    for k in sorted(langlinks.keys()):
        v = langlinks[k]
        print(f"{k}: {v.language} - {v.title}: {v.fullurl}")


print("Lang links:")
print_langlinks(page_py)
