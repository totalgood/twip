
# coding: utf-8

# In[ ]:

get_ipython().system(u'pip install gensim')
from gensim.models import Word2Vec


# # Loading a Model
# 
# Google trained the Word2Vec skipgram model on a ton of Google News articles  
# Model is 3G uncompressed so this will take a couple minutes, go get a coffee...  

# In[1]:

wv = Word2Vec.load_word2vec_format('/home/hobson/Downloads/GoogleNews-vectors-negative300.bin.gz', binary=True)


# In[34]:

wv.most_similar(positive=['king', 'woman'], negative=['man'])[:4]


# In[35]:

wv.most_similar(positive=['prince', 'woman'], negative=['man'])[:4]


# In[38]:

wv.most_similar(positive=['lord', 'royalty', 'woman'], negative=['man'])


# In[39]:

wv.most_similar(positive=['lord', 'manor', 'woman'], negative=['man'])


# In[33]:

wv.most_similar(positive=['queen', 'man'], negative=['woman'])[:4]


# # API
# 
# Not much documentation, so let's play!  
# Word2Vec can only handle lists of words  
# And words have to be in its vocabulary  

# # Quantified Self

# In[ ]:

list(w for w in wv.vocab if w.lower().startswith('quantified_'))
[u'quantified_emission',
 u'Quantified_Publisher',
 u'Quantified_Marketing_Group',
 u'Quantified_Analysis',
 u'Quantified_Publisher_program',
 u'Quantified_Self']
wv.most_similar(positive=['Quantified_Self', 'journal', 'diary'])
[(u'diaries', 0.679690957069397),
 (u'journals', 0.6234577894210815),
 (u'journal_Genome_Biology', 0.5596049427986145),
 (u'Preventing_Chronic_Disease', 0.5553246140480042),
 (u'journal_Rheumatology', 0.5511202216148376),
 (u'diary_entries', 0.5450901389122009),
 (u'Personall_warns', 0.5413833856582642),
 (u'journal_PNAS', 0.5409928560256958),
 (u'journal_Menopause', 0.5374890565872192),
 (u'journal_PLOS', 0.5371968150138855)]
wv.most_similar(positive=['journal', 'diary', 'python', 'semantic', 'NLP'])
[(u'journal_PNAS', 0.5335176587104797),
 (u'journals', 0.5311996340751648),
 (u'Personall_warns', 0.5287125110626221),
 (u'diaries', 0.5208494663238525),
 (u'Connotea', 0.5163055062294006),
 (u'PloS_Biology', 0.5094947218894958),
 (u'Wikipedia_encyclopedia', 0.5085359811782837),
 (u'journal_Neuropsychology', 0.5040772557258606),
 (u'journal_Behavioural_Ecology', 0.5029593110084534),
 (u'ontology', 0.5026495456695557)]
wv.most_similar(positive=['python', 'semantic_processing', 'meaning', 'NLP'])
wv.most_similar(positive=['python', 'semantic', 'processing', 'meaning', 'NLP'])
[(u'inferencing', 0.6100273132324219),
 (u'regex', 0.5578750371932983),
 (u'semantics', 0.5554606914520264),
 (u'semantic_indexing', 0.5523117184638977),
 (u'PCRE', 0.5505284667015076),
 (u'semantically', 0.543846845626831),
 (u'XML_namespaces', 0.5346047282218933),
 (u'Extensible_Application_Markup_Language', 0.5326448082923889),
 (u'phonemic', 0.5311585068702698),
 (u'Boolean_operators', 0.5305431485176086)]
wv.most_similar(positive=['Python', 'python', 'semantic', 'processing', 'meaning', 'NLP'])
[(u'inferencing', 0.6243683099746704),
 (u'PCRE', 0.6188617944717407),
 (u'regex', 0.6080276370048523),
 (u'parser', 0.5828561186790466),
 (u'XML_namespaces', 0.5820693373680115),
 (u'XML_parser', 0.5805317759513855),
 (u'XML_syntax', 0.5791804790496826),
 (u'TSQL', 0.5776033997535706),
 (u'DataWindow', 0.5756461024284363),
 (u'NET_CLR', 0.5726565718650818)]
wv.most_similar(positive=['Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install'])
[(u'NET_CLR', 0.6145628094673157),
 (u'PCRE', 0.6098397374153137),
 (u'swf_file', 0.6015275120735168),
 (u'TITLE_Debian_update', 0.5981236696243286),
 (u'inferencing', 0.5910664200782776),
 (u'XML_parser', 0.5868363380432129),
 (u'PHP_scripting', 0.5843981504440308),
 (u'HTML_CSS_JavaScript', 0.583228588104248),
 (u'remoting', 0.5813583731651306),
 (u'regex', 0.5790796279907227)]
wv.most_similar(positive=['Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular_expression'])
wv.most_similar(positive=['Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression'])
[(u'TSQL', 0.46374911069869995),
 (u'XML_XSLT', 0.46319350600242615),
 (u'HTML_CSS_JavaScript', 0.46195775270462036),
 (u'NET_CLR', 0.4589165151119232),
 (u'VisualBasic', 0.4558500051498413),
 (u'NET_framework', 0.454326868057251),
 (u'Perl_Python_Ruby', 0.4509257972240448),
 (u'inferencing', 0.44831690192222595),
 (u'mod_rewrite', 0.4465762674808502),
 (u'swf_file', 0.4453127682209015)]
wv.most_similar(positive=['Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft])
wv.most_similar(positive=['open_source', 'Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft'])
wv.most_similar(positive=['Open_Source', 'Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft'])
[(u'XML_XSLT', 0.4880766272544861),
 (u'HTML_CSS_JavaScript', 0.4751140773296356),
 (u'Java_JSP', 0.46583420038223267),
 (u'inferencing', 0.4654781222343445),
 (u'Perl_Python', 0.4650688171386719),
 (u'Perl_Python_Ruby', 0.4642208516597748),
 (u'TSQL', 0.458888977766037),
 (u'Actionscript', 0.45879411697387695),
 (u'mod_rewrite', 0.4582417905330658),
 (u'NET_framework', 0.4580802023410797)]
wv.most_similar(positive=['Cyc', 'OpenCog', 'Open_Source', 'Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft'])
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft'])
[(u'XML_XSLT', 0.5321134924888611),
 (u'Java_JSP', 0.5281328558921814),
 (u'inferencing', 0.5163978338241577),
 (u'HTML_CSS_JavaScript', 0.512594997882843),
 (u'Actionscript', 0.5115547180175781),
 (u'Object_Oriented', 0.5094218850135803),
 (u'Query_Language', 0.508894145488739),
 (u'mod_rewrite', 0.5063719749450684),
 (u'MochiKit', 0.5052181482315063),
 (u'NET_CLR', 0.5049869418144226)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft', 'TSQL'])
[(u'inferencing', 0.4273879826068878),
 (u'Assembler', 0.4221707284450531),
 (u'Literal_translation', 0.42108485102653503),
 (u'XML_XSLT', 0.420962393283844),
 (u'Java_JSP', 0.4199409484863281),
 (u'HTML_CSS_JavaScript', 0.4166453182697296),
 (u'Schrodinger', 0.416521817445755),
 (u'Actionscript', 0.4158591628074646),
 (u'Semantic', 0.4158053696155548),
 (u'Perl_Python', 0.41291189193725586)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'Natural_Language_Processing', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft', 'TSQL'])
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'natural_language', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft', 'TSQL'])
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chatterbot', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft', 'TSQL'])
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft', 'TSQL'])
[(u'Bing_Translator', 0.5751106142997742),
 (u'Python_programming', 0.5679047703742981),
 (u'inferencing', 0.5638830065727234),
 (u'processing_NLP', 0.5546227693557739),
 (u'XML_XSLT', 0.5532411336898804),
 (u'chatbots', 0.5529900193214417),
 (u'WordNet', 0.5514096617698669),
 (u'HTML_CSS_JavaScript', 0.5490512847900391),
 (u'HTML_CSS_Javascript', 0.5486903190612793),
 (u'mathematical_notation', 0.5454741716384888)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft', 'TSQL', 'Bing'])
[(u'inferencing', 0.5493630170822144),
 (u'processing_NLP', 0.5458688735961914),
 (u'XML_XSLT', 0.5446382761001587),
 (u'Python_programming', 0.542436957359314),
 (u'phonemic', 0.5351700186729431),
 (u'Bing_Translator', 0.533650279045105),
 (u'Ontologies', 0.5321763157844543),
 (u'Java_JSP', 0.5291105508804321),
 (u'Object_Oriented', 0.5287489295005798),
 (u'mathematical_notation', 0.5272959470748901)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['regex', 'regular', 'expression', 'Microsoft', 'TSQL', 'Bing', 'translate'])
[(u'inferencing', 0.5338713526725769),
 (u'XML_XSLT', 0.5273652076721191),
 (u'Ontologies', 0.5210939049720764),
 (u'processing_NLP', 0.5178764462471008),
 (u'Python_programming', 0.5158846378326416),
 (u'chatbots', 0.5153536200523376),
 (u'Java_JSP', 0.5145242214202881),
 (u'Bing_Translator', 0.5135848522186279),
 (u'Object_Oriented', 0.5110706090927124),
 (u'mathematical_notation', 0.5103068351745605)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'pip', 'install', 'grammar'], negative=['statistical'])
[(u'Python_programming', 0.6736586093902588),
 (u'PHP_scripting', 0.6660847663879395),
 (u'Bing_Translator', 0.6640334725379944),
 (u'regex', 0.6583566069602966),
 (u'NET_CLR', 0.6578915119171143),
 (u'semantic_markup', 0.657026469707489),
 (u'HTML_CSS_Javascript', 0.6541556715965271),
 (u'XML_syntax', 0.6483075618743896),
 (u'TITLE_Debian_update', 0.6467106938362122),
 (u'XML_XSLT', 0.6464080810546875)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'pip', 'install', 'statistical'], negative=['grammar'])
[(u'NET_CLR', 0.6777916550636292),
 (u'Bing_Translator', 0.6773670315742493),
 (u'PHP_scripting', 0.6669802665710449),
 (u'TITLE_Debian_update', 0.6665417551994324),
 (u'inferencing', 0.6656586527824402),
 (u'HTML_CSS_Javascript', 0.6646273136138916),
 (u'regex', 0.6629053354263306),
 (u'Python_programming', 0.6611731648445129),
 (u'NET_Remoting', 0.6532155871391296),
 (u'ASPX', 0.6508787870407104)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'statistical'], negative=['grammar'])
[(u'Bing_Translator', 0.6794119477272034),
 (u'inferencing', 0.6737903356552124),
 (u'regex', 0.669569194316864),
 (u'Python_programming', 0.6642642617225647),
 (u'HTML_CSS_Javascript', 0.6585268378257751),
 (u'XML_syntax', 0.6508367657661438),
 (u'semantic_indexing', 0.6507266759872437),
 (u'NET_CLR', 0.6478333473205566),
 (u'XML_eXtensible_Markup_Language', 0.6444374322891235),
 (u'Declarative', 0.6437892317771912)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'NLTK', 'statistical'], negative=['grammar'])
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'NLP', 'nltk', 'statistical'], negative=['grammar'])
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'statistical'], negative=['grammar'])
[(u'Bing_Translator', 0.6709335446357727),
 (u'regex', 0.6649294495582581),
 (u'inferencing', 0.6554071307182312),
 (u'Python_programming', 0.6519725322723389),
 (u'NET_CLR', 0.6503692269325256),
 (u'HTML_CSS_Javascript', 0.6472666263580322),
 (u'ASPX', 0.6460676789283752),
 (u'semantic_indexing', 0.6457715630531311),
 (u'PHP_scripting', 0.6413751244544983),
 (u'XML_syntax', 0.6399379968643188)]
wv.most_similar(positive=['Cyc', 'Cog', 'Open_Source', 'Python', 'python', 'semantic', 'Semantic', 'language', 'ai', 'chatbot', 'chat', 'processing', 'meaning', 'statistical', 'semantic_indexing'], negative=['grammar'])
[(u'Bing_Translator', 0.686427116394043),
 (u'regex', 0.6840069890022278),
 (u'inferencing', 0.6776837110519409),
 (u'NET_CLR', 0.6666378378868103),
 (u'ASPX', 0.6647640466690063),
 (u'TITLE_Debian_update', 0.6628689765930176),
 (u'PHP_scripting', 0.6614559888839722),
 (u'Python_programming', 0.6613916158676147),
 (u'HTML_CSS_Javascript', 0.6609216332435608),
 (u'XML_eXtensible_Markup_Language', 0.6534264087677002)]


# # Journal Summarization
# 
# Let's use state-of-the art Latent Dirichlet Allocation to preview a bunch of text files

# In[24]:

from pug.nlp import util
from gensim.summarization import summarize
import os.path


# In[12]:

tree = util.find_files('/home/hobson/Downloads/evernote_notes/', ext='.txt')
print(len(tree))
tree[0]


# # `summarize`
# 
# <img src="summarization_tutorial_plot.png">

# In[53]:

for meta in tree:
    if meta['name'].lower().startswith('stuff'):
        continue
    print('')
    print('-'*80)
    print('### ' + os.path.splitext(meta['name'])[0])
    text = os.path.splitext(meta['name'])[0] + '. \n' + open(meta['path']).read()
    try:
        summary = summarize(text, word_count=50)
    except ValueError:
        print('TOO SHORT to SUMMARIZE')
        summary = text[:200]
    try:
        print(' '.join(pair[0] for pair in wv.most_similar(positive=[w for w in summary.split() if w in wv.vocab])[1:5] if '%' not in pair[0])) 
    except ValueError:
        print('MISMATCHED VOCAB')
    print(summary)
    

