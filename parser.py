import json
import pprint
from tqdm import tqdm

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
        chem_annotations = []
        gene_annotations = []
        disease_annotations = []
        bacteria_annotations = []

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

            if len(passages) <= 1:
                continue
            else:
                for i in range(len(passages)):
                    # Check if annotation and text are contained in pasage
                    if 'text' in passages[i] and 'annotations' in passages[i] and 'offset' in passages[i]:
                        passage = passages[i]
                        text = passage['text']
                        annotations = passage['annotations']
                        offset = passage['offset']

                        if i==0:
                            title += text 
                        
                        else:
                            body += text + " "

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
                                start_char = annotation['locations'][0]["offset"] - offset
                                end_char = start_char + annotation['locations'][0]["length"]

                                annotation_output = "{} {}\t{}\t{}\t{}\n".format(pmid, start_char, end_char, annotation_text, annotation_type, annotation_identifier)
                                
                                if annotation_type == "Disease":
                                    disease_annotations.append(annotation_output)
                                elif annotation_type == "Chemical":
                                    chem_annotations.append(annotation_output)
                                elif annotation_type == "Bacteria":
                                    bacteria_annotations.append(annotation_output)
                                elif annotation_type == "Gene":
                                    gene_annotations.append(annotation_output)

                    elif i==0:
                        break
        # title = str(title.encode('utf-8'))
        # body = str(body.encode('utf-8'))

        # Append results to four output files
        if len(gene_annotations) > 0:
            gene_out.write(title)
            gene_out.write('\n')
            gene_out.write(body)
            gene_out.write('\n')
            for annotation in gene_annotations:
                gene_out.write(annotation)
            gene_out.write('\n')
            

        if len(chem_annotations) > 0:
            chem_out.write(title)
            chem_out.write('\n')
            chem_out.write(body)
            chem_out.write('\n')
            for annotation in chem_annotations:
                chem_out.write(annotation)
            chem_out.write('\n')
            

        if len(bacteria_annotations) > 0:
            bacteria_out.write(title)
            bacteria_out.write('\n')
            bacteria_out.write(body)
            bacteria_out.write('\n')
            for annotation in bacteria_annotations:
                bacteria_out.write(annotation)
            bacteria_out.write('\n')
            

        if len(disease_annotations) > 0:
            disease_out.write(title)
            disease_out.write('\n')
            disease_out.write(body)
            disease_out.write('\n')
            for annotation in disease_annotations:
                disease_out.write(annotation)
            disease_out.write('\n')
        
        pbar.update()