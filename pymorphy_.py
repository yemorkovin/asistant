import pymorphy2
morph = pymorphy2.MorphAnalyzer()
butyavka = morph.parse('бутявка')[0]
gent = butyavka.inflect({'gent'})
gent.word