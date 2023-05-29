import os

import openai
# from langchain import PromptTemplate

from util import get_mongo_collection, TermRelationshipName


if __name__ == "__main__":
    # openai.api_key = os.getenv("OPENAI_API_KEY")
    
    # messages = [ {"role": "system", 
    #               "content": "You are an intelligent agent that curates metadata for research studies in social and behavioral science."}, 
    #              {"role": "user", 
    #               "content": """Here is a summary of a study's subject matter:
    #               -----
    #               This study is a continuation of the 1974 Canadian Election Study, which consisted of extensive personal interviews with a national sample of 2,562 respondents following the federal election of July 8, 1974. Immediately following the federal election of May 22, 1979, 1,295 of the original respondents were successfully contacted and interviewed, thereby creating a 1974-1979 panel study. In addition, a new national sample of the l979 electorate and a supplementary sample of young voters (aged 18-23) were drawn and personal interviews utilizing the same questionnaire were conducted with respondents in these samples. After the federal election of February 18, 1980, 1,748 respondents in both the panel and cross-section samples were contacted by telephone and reinterviewed. No new respondents were added to the 1980 sample. When the Quebec referendum was called for May 20, 1980, a decision was made to contact by telephone Quebec respondents originally sampled in l974 or 1979 and interviewed in 1980. Of these respondents, 325 were successfully contacted and reinterviewed. Approximately half of the interviews were conducted immediately prior to the referendum, and the remaining half immediately afterward. The 1974 post-election survey covered a wide range of topics related to citizen participation in politics. The 1979 survey continued the theme of citizen interest and involvement in politics and probed respondents' attitudes about regions, provinces, and national unity. The 1980 telephone interview asked about vote choice in 1980, party identification, and the issue of energy. Questions on the Quebec referendum centered around the respondents' views on constitutional options for Quebec.
    #               -----
    #               Give me subject terms that indicate what the study is about. Subject Terms should follow the ICPSR Subject Terms Thesaurus. Simply give subject terms separated by commas.
    #               """} ]

    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=messages,
    #     max_tokens=1024,
    #     temperature=1
    # )

    # print(response["choices"][0]["message"]["content"])
    # subject_terms = response["choices"][0]["message"]["content"].split(",")
    subject_terms = "Canadian politics, Elections, Voting behavior, Citizen participation, Political attitudes, Regionalism, National unity, Party identification, Energy issues, Constitutional options, Quebec referendum"

    mongo_client, mongo_col = get_mongo_collection()
    for subj_term in subject_terms.split(","):
        subj_term = subj_term.strip().lower()
        res = mongo_col.find_one({"term_in_lowercase": subj_term})

        if res: # res is a dictionary
            print(f"Found predicted term: {res['term']}")

            for rel in TermRelationshipName:
                if rel.value in res:
                    print(f"{rel.value}: ", res[rel.value])
            print("-" * 30)
        else:
            print(f"Predicted term not in thesaurus: {subj_term}")
            print("-" * 30)
    
    mongo_client.close()
