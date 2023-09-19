import os
import PyPDF2
import pandas as pd

folder_path = 'data/data'

# list of folders in folders
items = os.listdir(folder_path)

content_list = ['additional information', 'certifications', 'interests', 'skills', 'technical skills', 'experience', 'languages', 'accomplishments', 'online profile', 'work experience', 'professional affiliations']

# excel file to save data
output_file = "resume_dataset.xlsx"
try:
    existing_data = pd.read_excel(output_file)
except FileNotFoundError:
    existing_data = pd.DataFrame(columns=['pdf_name', 'category', 'skills', 'education'])

dataframes_to_concat = []

# iterating through items list to find folders
for item in items:
    item_path = os.path.join(folder_path, item)  
    if os.path.isdir(item_path):  
        print('*'*25, f"{item}", '*'*25)  
        
        # iterating through subfolder
        subfolder_items = os.listdir(item_path)
        for subitem in subfolder_items:
            subitem_path = os.path.join(item_path, subitem)
            if subitem.endswith('.pdf'):
                print(subitem)  
                pdf_file = subitem_path
                
                # PDF reader object
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                
                education_list = []
                Skills_list = []
                
                # extracting text from the PDF pages
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    page_text = page_text.lower()
                    
                    # split page text into lines
                    lines = page_text.split('\n')
                    #print(len(lines))
                    #print(lines)
                    
                    # find skills and education from lines 
                    for line in lines:
                        if line == 'Skills' or line == 'Technical Skills':
                            index = lines.index(line)
                            skills_ele = lines[index+1:]
                            for s in skills_ele:
                                if s not in content_list:
                                    Skills_list.append(s)
                                else:
                                    break
                            
                        elif line == 'Education' or line == 'Education and Training' or line == 'Educational Background':
                            index = lines.index(line)
                            education_ele = lines[index+1:]
                            for edu in education_ele:
                                if edu not in content_list:
                                    education_list.append(edu)
                                else:
                                    break
                                
                # append data to the DataFrame 
                pdf_name = subitem.split(".")[0]
                category = item
                skills = ''.join(Skills_list)
                education = ''.join(education_list)
                if pdf_name or category or skills or education:
                    new_row = {'pdf_name': pdf_name, 'category': category, 'skills': skills, 'education': education}
                    new_dataframe = pd.DataFrame([new_row])
                    dataframes_to_concat.append(new_dataframe)
        
# concatenate the dataframes in the list and save data in excel file
if dataframes_to_concat:
    new_data = pd.concat(dataframes_to_concat, ignore_index=True)

    updated_data = pd.concat([existing_data, new_data], ignore_index=True)

    updated_data.to_excel(output_file, index=False)