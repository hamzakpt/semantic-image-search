from nltk import sent_tokenize
import re
import numpy as np
from scipy import spatial
import globals_var
import textacy
from more_itertools import unique_everseen
import pandas as pd
import hashlib
import os


def split_into_sentences(text):
    return sent_tokenize(text)


def avg_feature_vector(words, model, num_features):
    # function to average all words vectors in a given paragraph
    featureVec = np.zeros((num_features,), dtype="float32")
    nwords = 0
    # list containing names of words in the vocabulary
    # index2word_set = set(model.index2word) this is moved as input param for performance reasons
    for word in words:
        try:
            nwords = nwords + 1
            featureVec = np.add(featureVec, model[word])
        except (KeyError) as e:
            featureVec = np.add(featureVec, np.zeros(300))

    if (nwords > 0):
        featureVec = np.divide(featureVec, nwords)
    return featureVec

def parse_text(message, keywords):
    newList = []
    try:
        if len(keywords)==0:
            return []
        if len(message) == 0:
            return []


        message = message.replace('(','').replace(')','')
        for keyword in keywords:
            keyword = keyword.replace('(','').replace(')','')
            if re.search(r'\b{}\b'.format(keyword), message):
                newList.append(keyword)
    except(Exception) as e:
        print('error : ', e)
        print('message : ',message)
        print('keywords : ', keywords)
        pass
    return newList


# def build_inverted_index(texts):
#     inverted_index = {}
#     for i in range(len(texts)):
#         tokens = nltk.word_tokenize(texts[i].lower())
#         file_index = Counter(tokens)
#         # update global index
#         for term in file_index.keys():
#             file_freq = file_index[term]
#             if term not in inverted_index:
#                 inverted_index[term] = [file_freq, (i, file_freq)]
#             else:
#                 inverted_index[term][0] += file_freq
#                 inverted_index[term].append((i, file_freq))

#     return inverted_index

def string_matching_word2vec(text_to_match, sentences, model, threshold=0.80, is_substring=False):
    original_sentences = sentences
    text_to_match = re.sub(r"\d+", " ", text_to_match)

    # print('*********************************************WORD2VEC ')
    # print('original_sentences:::::::::: ',original_sentences)

    digit = False
    try:

        if text_to_match.replace('.', '').replace('-', '').replace(' ', '').replace('(', '').replace(')',
                                                                                                     '').strip().isdigit():
            digit = True
        if digit:
            return []
    except(Exception) as e:
        # print("Exception in exact string macth: ", e, " | ", digit)
        pass

    if is_substring:
        sub_string_original_sentences = sentences
        sentences = list(filter(None, [s and s.replace('-', ' ').strip() for s in sentences]))
        s = text_to_match.replace('-', ' ').replace('.', '')
        result = []
        temp_sentences = []
        text_to_match = s.strip()
        if len(text_to_match) <= 1:
            return []
        length = len(text_to_match.split())
        sentences = sentences[::-1]
        for index, each in enumerate(sentences):
            index = len(sentences) - index - 1
            temp = []
            each = each.replace('-', ' ').replace('.', '')

            if len(each) <= 1:
                del sub_string_original_sentences[index]
                continue
            text = each.split()
            j = length
            if (len(text) >= length):
                # print('********************* Substring slicing')
                for i in range(len(text)):

                    if len(text[i:j]) == length:
                        temp.append(' '.join(text[i:j]))
                    else:
                        break
                    j += 1
            else:
                del sub_string_original_sentences[index]
                continue
            if len(temp) > 0:
                result.append(temp)
                temp_sentences += temp
            else:
                del sub_string_original_sentences[index]

        sentences = list(set(temp_sentences))
        original_sentences = sentences
        sub_string_original_sentences = sub_string_original_sentences[::-1]
        # print('List of list ::::: ',result)
        # print('Sentences::::::::::: ',sentences)
        String_split = [text_to_match]
    else:
        String_split = list(
            filter(None, [
                s and s.replace('.', '')
                for s in split_into_sentences(text_to_match)
            ]))

    matched_substrings = []
    # print('***************************************************')
    # print('String Compare:::: text_to_match:::  ', text_to_match)
    # print('String Compare:::: String_split::: ', String_split)
    # print('+++++++++++++++++++++++++++++++++++++++++++++++++++')

    counter = 0
    sentences_to_match = []

    s_vector = []  # Average sentence vectors list
    for s in String_split:
        s = ' '.join([globals_var.wordnet_lemmatizer.lemmatize(word) for word in s.split()]).lower()
        s = ' '.join([(word) for word in s.split() if word not in globals_var.stop_words])

        # s = ' '.join([wordnet_lemmatizer.lemmatize(word) for word in s.split() if word not in stop_words]).lower()
        # print('sssssssssss:   ',s)
        step1 = textacy.preprocess_text(s, no_currency_symbols=True, no_numbers=True, no_punct=True,
                                        fix_unicode=True, no_contractions=True)
        step2 = textacy.preprocess.fix_bad_unicode(step1)
        step3 = textacy.preprocess.transliterate_unicode(step2).strip().replace('.', '').lower()
        # print('Step3:::::: ',step3)
        if (len(step3) > 1):
            sentences_to_match.append(step3)
            s_vector.append(avg_feature_vector(step3.split(), model, 300))
            counter += 1
    if len(sentences_to_match) == 0:
        return []

    # sentences = list(
    #     unique_everseen(
    #         filter(None, [
    #             s and
    #                          s.strip()
    #             for s in sentences
    #         ])))

    temp_sentences = []
    sentences_vector = []
    sentences = sentences[::-1]
    for index, each in enumerate(sentences):
        index = len(sentences) - 1 - index
        each = re.sub(r"\d+", " ", each).strip()
        each = ' '.join([globals_var.wordnet_lemmatizer.lemmatize(word) for word in each.split()]).lower()
        each = ' '.join([(word) for word in each.split() if word not in globals_var.stop_words])
        step1 = textacy.preprocess_text(each, no_currency_symbols=True, no_numbers=True, no_punct=True,
                                        fix_unicode=True, no_contractions=True)
        step2 = textacy.preprocess.fix_bad_unicode(step1)
        step3 = textacy.preprocess.transliterate_unicode(step2).strip().replace('.', '').lower()

        if len(step3) > 1:
            temp_sentences.append(step3)
            sentences_vector.append(avg_feature_vector(
                step3.split(), model,
                300))
        else:
            del original_sentences[index]

    temp_sentences = temp_sentences[::-1]
    final_sentences = temp_sentences
    sentences_vector = sentences_vector[::-1]

    # if is_substring:
    #     original_sentences = final_sentences

    i = 0  # control text_to_match

    # print('original_sentences::::::: ',original_sentences)
    # print('Lenghthhhhhhhhhhhh ',len(original_sentences) , ' :::::::: ',len(final_sentences))
    # print('****************************')

    # for ii,each in enumerate(original_sentences):
    #     print(each , '"""""""""""',final_sentences[ii])
    #
    # print('****************************')
    matched_sentences = []
    temp_matched_sentences = []
    yes_scores = []
    highest_score = 0
    temp_substrings = []
    temp_score = []

    for j, sent in enumerate(final_sentences):
        # print(sent ,'"::::::::::::::::: ',sentences_to_match[i])
        Found = False
        sentence_vector = sentences_vector[j]  # convert sentencesument sentence to vec

        if (len(s_vector) == 0):
            score = 0
        else:
            score = 1 - spatial.distance.cosine(s_vector[i], sentence_vector)
        # print('Score::::::::::::::::::: ',score)

        if (score > threshold):
            # print('matched with usign word2vec  ::: ', sent, '    score::: ', score)
            if len(original_sentences[j]) > 1:
                temp_matched_sentences.append(original_sentences[j])
                temp_score.append(score)
                Found = True

        if i == len(sentences_to_match) - 1:
            if (Found == True):
                score = sum(temp_score) / len(temp_score)

                # print('Found in word2vec:::::::::::::: ',temp_matched_sentences)
                if highest_score < score:
                    matched_sentences = temp_matched_sentences + matched_sentences

                    yes_scores = [score] + yes_scores
                else:
                    matched_sentences = matched_sentences + temp_matched_sentences
                    yes_scores.append(score)
                if highest_score < score:
                    highest_score = score
                matched_substrings += temp_matched_sentences

            i = 0
            temp_matched_sentences = []
            temp_score = []

        else:
            if (Found):
                i = i + 1
                continue
        if (Found == False):
            i = 0
            temp_matched_sentences = []
            temp_score = []

    if len(matched_sentences) > 0:
        # temp_matched_sentences = set(matched_sentences)
        no = []
        # print('yes::::::::::: ',matched_sentences)

        yes = matched_sentences
        if is_substring:
            temp_yes = []
            # print('sub_string_original_sentences:::::::::: ',sub_string_original_sentences)
            # print('Result:::::::::: ',result)
            for each in yes:
                for index, sen in enumerate(result):
                    if len(each) > 1:
                        if each in sen:
                            # print('sub_string_original_sentences[index] L:::::::::::: ',sub_string_original_sentences[index])
                            temp_yes.append(sub_string_original_sentences[index])
            yes = list(set(temp_yes))
        # print('Final::::::::::::: ',yes)
        return [yes, no, yes_scores, matched_substrings]
    #     print("returning 241")
    return matched_sentences


def get_data_from_database():
    images = []
    texts = []
    category = []
    all_records = globals_var.db.images_data.find({})
    for record in all_records:
        images.append(record["image_path"])
        category.append(record["category"])
        texts.append(record["text"])
    return images, texts, category

def sub_string_matching(text_to_match, threshold=0.50):

    model = globals_var.model
    sentences = globals_var.texts
    # print('********************** Sub String')

    digit = False
    try:

        if text_to_match.replace('.', '').replace('(', '').replace(')', '').strip().isdigit():
            digit = True

    except(Exception) as e:
        # print("Exception in exact string macth: ", e, " | ", digit)
        pass



    original_text_to_match = text_to_match
    # print('text_to_match::: ', text_to_match)

    # print('text_to_match::: ', text_to_match)
    text_sentences = list(
        unique_everseen(filter(None, [s and s.strip().replace('.', '') for s in split_into_sentences(text_to_match)])))
    text_tokens = [list(filter(None, [s and s.strip() for s in x.split()])) for x in text_sentences]


    if len(text_sentences) == 0:
        return []

    if len(sentences) == 0:
        return []

    sentences = list(unique_everseen(filter(None, [s and s.strip() for s in sentences])))
    sentences_token = [set(filter(None, x.replace('.', '').lower().split())) for x in sentences]
    matched_sentences = []
    Found = False
    # print('************************************* Sub String')
    # print('text_sentences::: ', text_sentences)
    # print('sentences::: ', sentences)

    yes_scores = []
    matched_substrings = []
    temp_text_found = []
    temp_matched_substrings = []
    i = 0
    for j, text in enumerate(sentences):
        Found = False
        # text = ' '.join([wordnet_lemmatizer.lemmatize(word) for word in text.split() if word not in stop_words]).strip().lower()
        if (len(text_sentences) > 0):
            temp_text = text_sentences[i]
            text_token = text_tokens[i]

            if (len(text.strip()) > 0):
                text = text.lower().replace('.', '')
                sen_token = sentences_token[j]

                if len(temp_text) < len(text):
                    if len(parse_text(text, [temp_text])) > 0:
                        temp_text_found.append(sentences[j])
                        Found = True
                        temp_matched_substrings.append(text_sentences[i])

                else:
                    if len(parse_text(temp_text, [text])) > 0:
                        temp_text_found.append(sentences[j])
                        Found = True
                        temp_matched_substrings.append(text_sentences[i])



        else:
            break

        if (i == len(text_sentences) - 1):
            if Found:
                matched_sentences += temp_text_found
                # print("temp_matched_substrings:: : ", temp_matched_substrings)
                matched_substrings += temp_matched_substrings
                yes_scores.append(1)
            temp_text_found = []
            temp_matched_substrings = []
            i = 0
            continue

        elif (Found == False):
            i = 0
            temp_text_found = []
            temp_matched_substrings = []
        else:
            i += 1

    if len(matched_sentences) == 0 and digit == False:
        # print('Sending Data to Word2Vec to Substring ***********************************+++++++++++++')
        return string_matching_word2vec(original_text_to_match, sentences, model, threshold, is_substring=True)

    if (len(matched_sentences) > 0):
        # print('matched_sentences:::::::::: Direct Sub String ',matched_sentences)
        # matched_sentences = set(matched_sentences)
        # no = list(set(sentences) - matched_sentences)
        yes = matched_sentences
        return [yes, [], yes_scores, matched_substrings]
    else:
        return []


# Process result in way (text, [matching pairs of words], average score)
def process_result(result):
    # print("result: :: : ", result)
    temp_dic = {}
    if result:
        for score, substring in zip(result[2], result[3]):
            for txt in result[0]:
    #             print("substring:: ", substring)
    #             print("txt:: : ", txt)
                if substring in txt:
                    if txt not in temp_dic:
                        temp_dic[txt] = {} ; temp_dic[txt]["strings"] = []
                        temp_dic[txt]["scores"] = []
                    temp_dic[txt]["strings"].append(substring)
                    temp_dic[txt]["scores"].append(score)
    # Now we have to find the average score for each key
    # converting into lists
    scores = []
    substrings = []
    texts = []
    for key in temp_dic.keys():
        texts.append(key)
        score  = temp_dic[key]["scores"]
        scores.append(sum(score)/len(score))
        substrings.append(temp_dic[key]["strings"])
    return texts, substrings, scores

def get_top_images(query, k=5):
    result = sub_string_matching(query, threshold=0.6)
    texts, substrings, scores = process_result(result)
    query_data = pd.DataFrame()
    query_data["texts"] = texts
    query_data["substrings"] = substrings
    query_data["scores"] = scores
    sorted_data = query_data.sort_values("scores", ascending=False).reset_index()
    # Now we have text that is matched
    # Now we have to find the index of text in orginal text
    score, top_texts = list(sorted_data["scores"]), list(sorted_data["texts"])
    matched_images = []
    for text, sc in zip(top_texts, score):
        index = globals_var.texts.index(text)
        if index !=-1:
            matched_images.append({
                "image": globals_var.images[index],
                "score": sc
            })
    return matched_images


def mean_avg_precision(search_results, relevance):
    # TODO: calculate MAP score for search results, treating relevance judgments as binary - either relevant or not.
    #
    # search_results: list of lists of ranked results for each query [[doc_id1, doc_id2,...], ...]
    # note that for tests to pass, the i-th result in search_results should correspond to (i+1)-th query_id.
    # relevance: dict, query_id:[(relevant_doc_id1, score1), (relevant_doc_id2, score2), ...]
    mean_percision = []
    for index in range(len(search_results)):
        query_id = index + 1
        relevant_doc_id = []
        relevant_doc_id = relevance
        # NOw we have ids
        precision = []
        sum_rel = 0
        result_found = 0
        for result in search_results[index]:
            # print("Result: ", result)
            # print("relevant_doc_id: ", relevant_doc_id)
            # return
            if result["image"] in relevant_doc_id:
                result_found += 1
                prec = result_found / (len(precision) + 1)
                precision.append(prec)
                sum_rel += prec
            else:
                precision.append(result_found / (len(precision) + 1))
        if len(relevant_doc_id) != 0:
            mean_percision.append(sum_rel / len(relevant_doc_id))
        else:
            mean_percision.append(0)
        # print("precision::  ", precision)

        # print("relevant_doc_id:: ", relevant_doc_id)
    return sum(mean_percision) / len(search_results)

def calcualte_map():
    csv_url = globals_var.csv_path
    df =pd.read_csv(csv_url)
    categories = list(set(list(df["category"])))
    for cate in categories:
        # Now we have each category
        # Grab all the images from this category from database
        data = globals_var.db.images_data.find({"category": cate})
        relevant_documents = []
        for d in data:
            img_url = d["image_path"]
            relevant_documents.append(img_url)
        # Now we have relevant document
        # Now search for that category and retrive documents
        # Top 10 document
        if cate in globals_var.queries.keys():

            cate = globals_var.queries[cate]

        top_10_documents = get_top_images(cate, k=10)

        search_results = []
        for res in top_10_documents:

            search_results.append(res["image"])
        if cate =="airplanes":
            print("[top_10_documents]: ", [top_10_documents])
            print("relevant_documents:: : ", relevant_documents)
            map = mean_avg_precision([top_10_documents], search_results)
            print("result: ", map,  " : category : ", cate)


def md5(fname):
    """
    function used to create file hash
    :param fname:
    :return: file hash
    """
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    hash_value = hash_md5.hexdigest()
    return hash_value


def get_file_name_and_type(file):
    file_name_without_extension = ".".join(file.split(".")[:-1])
    file_type = file.split(".")[-1]
    return file_name_without_extension, file_type


def upload_image(image_raw, file_directory):
    upload_path = os.path.normpath(file_directory)
    try:
        if not os.path.exists(upload_path):
            os.makedirs(upload_path)

        upload_image_file = os.path.join(upload_path, image_raw.filename)
    
        file_name, file_type = get_file_name_and_type(image_raw.filename)
        size = 0
        with open(upload_image_file, 'wb') as out:
            while True:
                data = image_raw.file.read(8192)
                if not data:
                    break
                out.write(data)
                size += len(data)
        file_hash = md5(upload_image_file)
        os.rename(upload_image_file,
                  os.path.join(upload_path,
                               file_hash + '.' + file_type))
        return os.path.join(upload_path,
                               file_hash + '.' + file_type)
    except Exception as e:
        return str(e)
