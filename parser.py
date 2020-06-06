import json
import pprint
from tqdm import tqdm

# Minimum length of an article = 1 title + 1 body paragraph = 2
ARTICLE_MINIMUM_LENGTH = 2

gene_out = open('gene_lpsn.litcovid.pubtator', 'a')
chem_out = open('chem_lpsn.litcovid.pubtator', 'a')
disease_out = open('disease_lpsn.litcovid.pubtator', 'a')
bacteria_out = open('bacteria_lpsn.litcovid.pubtator', 'a')

with open("./litcovid2pubtator.json") as f:
    # Load json data
    data = json.load(f)

    # Get articles
    articles = data[1]

    # Initialize progress bar
    pbar = tqdm(total = len(articles))

    for article in articles:
        title = ""
        body = ""

        # Check if passages are contained in article dict
        if 'passages' in article:
            passages = article['passages']

            # Check if article as a pmid
            if 'pmid' in article:
                pmid = article['pmid']
            else:
                pmid = -1
            title = "{}|t|".format(pmid)
            body = "{}|a|".format(pmid)

            if len(passages) <= ARTICLE_MINIMUM_LENGTH:
                pbar.update()
                continue

            # Construct title line and store title_length
            else:
                title_length = 0
                if 'text' in passages[0] and 'offset' in passages[0]: 
                    title += passages[0]['text']
                    title = str(title)
                    title_length = len(passages[0]['text'])+1
                        

                for i in range(len(passages)):
                    if i == 0:
                        pbar.update()
                        continue
                    chem_annotations = []
                    gene_annotations = []
                    disease_annotations = []
                    bacteria_annotations = []

                    # Check if annotation and text are contained in pasage
                    if 'text' in passages[i] and 'annotations' in passages[i] and 'offset' in passages[i]:
                        passage = passages[i]
                        text = passage['text']
                        annotations = passage['annotations']
                        offset = passage['offset']
                
                        curr_body = body+text
                        curr_body = str(curr_body)

                        for annotation in annotations:
                            if 'infons' in annotation\
                                and 'type' in annotation['infons']\
                                and 'identifier' in annotation['infons']\
                                and 'text' in annotation\
                                and 'locations' in annotation \
                                and 'length' in annotation['locations'][0]\
                                and 'offset' in annotation['locations'][0]:

                                annotation_text = annotation['text']
                                annotation_type = annotation['infons']['type']
                                annotation_identifier = annotation['infons']['identifier']
                                start_char = annotation['locations'][0]["offset"] - offset + title_length
                                end_char = start_char + annotation['locations'][0]["length"]

                                annotation_output = "{}\t{}\t{}\t{}\t{}\n".format(pmid, start_char, end_char, annotation_text, annotation_type, annotation_identifier)
                            
                                if annotation_type == "Disease":
                                    disease_annotations.append(annotation_output)
                                elif annotation_type == "Chemical":
                                    chem_annotations.append(annotation_output)
                                elif annotation_type == "Bacteria":
                                    bacteria_annotations.append(annotation_output)
                                elif annotation_type == "Gene":
                                    gene_annotations.append(annotation_output)

                         # Append results to four output files
                        if len(gene_annotations) > 0 and len(curr_body) > len(body):
                            gene_out.write(title)
                            gene_out.write('\n')
                            gene_out.write(curr_body)
                            gene_out.write('\n')
                            for annotation in gene_annotations:
                                gene_out.write(annotation)
                            gene_out.write('\n')
                            

                        if len(chem_annotations) > 0 and len(curr_body) > len(body):
                            chem_out.write(title)
                            chem_out.write('\n')
                            chem_out.write(curr_body)
                            chem_out.write('\n')
                            for annotation in chem_annotations:
                                chem_out.write(annotation)
                            chem_out.write('\n')
                            

                        if len(bacteria_annotations) > 0 and len(curr_body) > len(body):
                            bacteria_out.write(title)
                            bacteria_out.write('\n')
                            bacteria_out.write(curr_body)
                            bacteria_out.write('\n')
                            for annotation in bacteria_annotations:
                                bacteria_out.write(annotation)
                            bacteria_out.write('\n')
                            

                        if len(disease_annotations) > 0 and len(curr_body) > len(body):
                            disease_out.write(title)
                            disease_out.write('\n')
                            disease_out.write(curr_body)
                            disease_out.write('\n')
                            for annotation in disease_annotations:
                                disease_out.write(annotation)
                            disease_out.write('\n')
                        
        pbar.update()
        
    
    # passages = articles[5]["passages"]
    # for passage in passages:
    #     offset = passage['offset']
    #     full_text = passage['text']

    #     if "annotations" in passage:
    #         annotations = passage['annotations']
    #         for annotation in annotations:
    #             text = annotation["text"]
    #             index = annotation['locations'][0]["offset"]
    #             length = annotation['locations'][0]["length"]
    #             # print(full_text)
    #             # print(text)
    #             # print(index-offset)
    #             # print(length)
    #             # print()
    #             print(text)
    #             string = ""
                # for i in range(length):
                #     string += full_text[index-offset+i]
                # print(string)

# string = "Rifampin and rifaximin resistance in clinical isolates of Clostridium difficile. Rifaximin, a poorly absorbed rifamycin derivative, is a promising alternative for the treatment of Clostridium difficile infections. Resistance to this agent has been reported, but no commercial test for rifaximin resistance exists and the molecular basis of this resistance has not been previously studied in C. difficile. To evaluate whether the rifampin Etest would be a suitable substitute for rifaximin susceptibility testing in the clinical setting, we analyzed the in vitro rifaximin susceptibilities of 80 clinical isolates from our collection by agar dilution and compared these results to rifampin susceptibility results obtained by agar dilution and Etest. We found rifaximin susceptibility data to agree with rifampin susceptibility; the MICs of both antimicrobials for all isolates were either very low or very high. Fourteen rifaximin-resistant (MIC, > or = 32 microg/ml) unique isolates from patients at diverse locations in three countries were identified. Molecular typing analysis showed that nine (64%) of these isolates belonged to the epidemic BI/NAP1/027 group that is responsible for multiple outbreaks and increased disease severity in the United Kingdom, Europe, and North America. The molecular basis of rifaximin and rifampin resistance in these isolates was investigated by sequence analysis of rpoB, which encodes the beta subunit of RNA polymerase, the target of rifamycins. Resistance-associated rpoB sequence differences that resulted in specific amino acid substitutions in an otherwise conserved region of RpoB were found in all resistant isolates. Seven different RpoB amino acid substitutions were identified in the resistant isolates, which were divided into five distinct groups by restriction endonuclease analysis typing. These results suggest that the amino acid substitutions associated with rifamycin resistance were independently derived rather than disseminated from specific rifamycin-resistant clones. We propose that rifaximin resistance in C. difficile results from mutations in RpoB and that rifampin resistance predicts rifaximin resistance for this organism."
# for i in range(180,201,1):
#     print(string[i])