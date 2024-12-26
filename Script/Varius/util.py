import re
import numpy as np
alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov|edu|me)"
digits = "([0-9])"
multiple_dots = r'\.{2,}'


def extract_KG_text(df_tot, answer_entities):
  KG_text=[]
  for i in range(len(answer_entities)):
    for j in range(len(answer_entities[i])):
      for z in range(len(df_tot['answer'])):

        if (answer_entities[i][j] in df_tot['answer'][z] and z!=i and not([df_tot['answer'][i],"rel",df_tot['answer'][z]] in KG_text) and not([df_tot['answer'][z],"rel",df_tot['answer'][i]] in KG_text)):

          KG_text.append([df_tot['answer'][i],"rel",df_tot['answer'][z]])


  return KG_text

def extract_text_entities(possible_candidates_baseline, model_BERT, question_entities, answer_entities, df_tot, answer_enc):

  possible_candidates=[]
  possible_candidates_enc=[]


  kg_text=[]

  for i in range(len(question_entities)):

    list_candiates=[]
    list_candiates_enc=[]

    list_candiates.append(possible_candidates_baseline[i][0])
    list_candiates_enc.append(model_BERT.text_emebedding(possible_candidates_baseline[i][0]))

    for j in range(len(question_entities[i])):

      for r in range(len(answer_entities)):

        for k in range(len(answer_entities[r])):

            if (question_entities[i][j] == answer_entities[r][k] and not (df_tot['answer'][r] in list_candiates)):

              list_candiates.append(df_tot['answer'][r])
              list_candiates_enc.append(answer_enc[r])

    if(len(list_candiates)<1):

      list_candiates=df_tot['answer'].tolist()
      list_candiates_enc=answer_enc

    possible_candidates.append(list_candiates)
    possible_candidates_enc.append(list_candiates_enc)

  return possible_candidates, possible_candidates_enc


def extract_entities(question,list_KB_clean,possible_candidates_baseline_order):
  question_entities=[]
  answer_entities=[]

  for i in range(len(question)):

    question_entity=[]
    answer_entity=[]

    for j in range(len(list_KB_clean)):

      for z in range(len(list_KB_clean[j])):

        if list_KB_clean[j][z][0] in possible_candidates_baseline_order[i][0]:

          answer_entity.append(list_KB_clean[j][z][2])

        if list_KB_clean[j][z][2] in possible_candidates_baseline_order[i][0]:

          answer_entity.append(list_KB_clean[j][z][0])

        if list_KB_clean[j][z][0] in question[i]:

          question_entity.append(list_KB_clean[j][z][2])

        if list_KB_clean[j][z][2] in question[i]:

          question_entity.append(list_KB_clean[j][z][0])


    question_entities.append(list(set(question_entity)))
    answer_entities.append(list(set(answer_entity)))
  

  return question_entities, answer_entities

def create_similarity_matrix_KB(question_enc, answer_enc):
  scores_similarity=[]

  for i in range(len(question_enc)):

    score_similarity=[]

    for j in range(len(possible_candidates_enc[i])):

      score_similarity.append(np.dot(question_enc[i], possible_candidates_enc[i][j]))

    scores_similarity.append(score_similarity)

  return scores_similarity

def create_similarity_matrix(question_enc, answer_enc):
  scores_similarity=[]
  for i in range(len(question_enc)):
    score_similarity=[]
    for j in range(len(answer_enc)):
      if base:
        score_similarity.append(np.dot(question_enc[i], answer_enc[j]))
      else:
        score_similarity.append(np.dot(question_enc[i], answer_enc[i][j]))


    scores_similarity.append(score_similarity)
  return scores_similarity

def order_candidate(scores_similarity, answer):
  list_scores=[]
  possible_candidates_baseline_order=[]
  for i in range(len(scores_similarity)):
    list_score, list_candidate_baseline = zip(*sorted(zip(scores_similarity[i],answer), reverse=True))
    list_scores.append(list_score)
    possible_candidates_baseline_order.append(list(dict.fromkeys(list_candidate_baseline)))

  return list_scores, possible_candidates_baseline_order

def evaluation_function(possible_candidates_baseline_order,answer):
  for j in [1,3,5,10,15,20]:
    correct=0
    for i in range(len(possible_candidates_baseline_order)):
      if answer[i] in possible_candidates_baseline_order[i][:j]:
        correct+=1
    print("Top "+str(j),correct/len(possible_candidates_baseline_order))
  print("----------------")



def save_network_html(list_enti, list_kb_flat, filename="network.html"):
    # create network
    net = Network(directed=True, width="auto", height="700px", bgcolor="#eeeeee")

    # nodes
    color_entity = "#00FF00"
    for e in list_enti:
        net.add_node(e, shape="circle", color=color_entity)

    # edges
    for r in list_kb_flat:
        net.add_edge(r[0], r[2],
                    title=r[1], label=r[1])

    # save network
    net.repulsion(
        node_distance=200,
        central_gravity=0.2,
        spring_length=200,
        spring_strength=0.05,
        damping=0.09
    )
    net.set_edge_smooth('dynamic')
    net.show(filename)

def split_into_sentences(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]: sentences = sentences[:-1]
    return sentences