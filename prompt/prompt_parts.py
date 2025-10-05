INTRODUCTION = """
                    Given a query and a document, you must provide a score on an integer scale of 0 to 2 with the following meanings:
                    2 = highly relevant, very helpful for this query 
                    1 = relevant, may be partly helpful but might contain other irrelevant content 
                    0 = not relevant, should never be shown for this query 
                    Assume that you are writing a report on the subject of the topic. 
                    If you would use any of the information contained in the document in such a report, mark it 1.
                    If the document is primarily about the topic, or contains vital information about the topic, mark it 2. Otherwise, mark it 0.
                """

OUTPUT_EXAMPLE = """
                    [{"O" : 1}]
                    Results [{
                """

OUTPUT_EXAMPLE_MULTIPLE = """
                    [{"M" : 2, "T" : 1, "O" : 1}]
                    Results [{
                """

ASPECT = """
            Measure how well the content matches a likely intent of the query(M).
            Measure how trustworthy the web page is (T).
            Consider the aspect above and the relative importance of each, and decide on a final score(O). 
         """

NON_ASPECT = "Decide on a final score(O)."

COVID_QUERY_BASED_EXAMPLE = """
                            Query：influenza duration
                            Document：Influenza, commonly known as the flu, is an infectious disease caused by influenza viruses. Symptoms range from mild to severe and often include fever, runny nose, sore throat, muscle pain, headache, coughing, and fatigue. These symptoms begin one to four (typically two) days after exposure to the virus and last for about two to eight days. Diarrhea and vomiting can occur, particularly in children. Influenza may progress to pneumonia from the virus or a subsequent bacterial infection. Other complications include acute respiratory distress syndrome, meningitis, encephalitis, and worsening of pre-existing health problems such as asthma and cardiovascular disease.
                            Definition sentence：Influenza is a contagious respiratory illness caused by influenza viruses, characterized by symptoms such as fever, cough, sore throat, muscle aches, and fatigue, with potential complications including pneumonia and exacerbation of existing health conditions.
                        """

COVID_NAMED_ENTITY_BASED_EXAMPLE = """
                            Named Entity：influenza
                            Document：Influenza, commonly known as the flu, is an infectious disease caused by influenza viruses. Symptoms range from mild to severe and often include fever, runny nose, sore throat, muscle pain, headache, coughing, and fatigue. These symptoms begin one to four (typically two) days after exposure to the virus and last for about two to eight days. Diarrhea and vomiting can occur, particularly in children. Influenza may progress to pneumonia from the virus or a subsequent bacterial infection. Other complications include acute respiratory distress syndrome, meningitis, encephalitis, and worsening of pre-existing health problems such as asthma and cardiovascular disease.
                            Definition sentence：Influenza is a contagious respiratory illness caused by influenza viruses, characterized by symptoms such as fever, cough, sore throat, muscle aches, and fatigue, with potential complications including pneumonia and exacerbation of existing health conditions.
                        """

COVID_LLM_QUERY_BASED_EXAMPLE = """
                            Query：influenza duration
                            Definition sentence：Influenza is a contagious respiratory illness caused by influenza viruses, characterized by symptoms such as fever, cough, sore throat, muscle aches, and fatigue, with potential complications including pneumonia and exacerbation of existing health conditions.
                        """

ROBUST_QUERY_BASED_EXAMPLE = """
                            Query：NRA membership profile
                            Document：The National Rifle Association of America (NRA) is a gun rights advocacy group based in the United States. Founded in 1871 to advance rifle marksmanship, the modern NRA has become a prominent gun rights lobbying organization while continuing to teach firearm safety and competency. The organization also publishes several magazines and sponsors competitive marksmanship events. The group claimed nearly 5 million members as of December 2018, though that figure has not been independently confirmed. 
                            Definition sentence：The National Rifle Association (NRA) is a U.S.-based organization founded in 1871 that advocates for gun rights, promotes firearm safety and competency, and sponsors marksmanship events.
                        """

ROBUST_NAMED_ENTITY_BASED_EXAMPLE = """
                            Named Entity：NRA
                            Document：The National Rifle Association of America (NRA) is a gun rights advocacy group based in the United States. Founded in 1871 to advance rifle marksmanship, the modern NRA has become a prominent gun rights lobbying organization while continuing to teach firearm safety and competency. The organization also publishes several magazines and sponsors competitive marksmanship events. The group claimed nearly 5 million members as of December 2018, though that figure has not been independently confirmed. 
                            Definition sentence：The National Rifle Association (NRA) is a U.S.-based organization founded in 1871 that advocates for gun rights, promotes firearm safety and competency, and sponsors marksmanship events.
                        """

ROBUST_LLM_QUERY_BASED_EXAMPLE = """
                            Query：NRA membership profile
                            Definition sentence：The National Rifle Association (NRA) is a U.S.-based organization founded in 1871 that advocates for gun rights, promotes firearm safety and competency, and sponsors marksmanship events.
                        """

NFCORPUS_QUERY_BASED_EXAMPLE = """
                            Query：Treatment for bronchiolitis obliterans
                            Document：Bronchiolitis obliterans (BO), also known as obliterative bronchiolitis, constrictive bronchiolitis and popcorn lung, is a disease that results in obstruction of the smallest airways of the lungs (bronchioles) due to inflammation. Symptoms include a dry cough, shortness of breath, wheezing and feeling tired. These symptoms generally get worse over weeks to months. It is not related to cryptogenic organizing pneumonia, previously known as bronchiolitis obliterans organizing pneumonia.While the disease is not reversible, treatments can slow further worsening. This may include the use of corticosteroids or immunosuppressive medication. A lung transplant may be offered. Outcomes are often poor, with most people dying in months to years.
                            Definition sentence：Bronchiolitis obliterans (BO) is a lung disease characterized by inflammation and obstruction of the smallest airways (bronchioles), leading to symptoms like dry cough, shortness of breath, and fatigue, with progressive worsening over time.
                        """

NFCORPUS_NAMED_ENTITY_BASED_EXAMPLE = """
                            Named Entity：bronchiolitis obliterans
                            Document：Bronchiolitis obliterans (BO), also known as obliterative bronchiolitis, constrictive bronchiolitis and popcorn lung, is a disease that results in obstruction of the smallest airways of the lungs (bronchioles) due to inflammation. Symptoms include a dry cough, shortness of breath, wheezing and feeling tired. These symptoms generally get worse over weeks to months. It is not related to cryptogenic organizing pneumonia, previously known as bronchiolitis obliterans organizing pneumonia.While the disease is not reversible, treatments can slow further worsening. This may include the use of corticosteroids or immunosuppressive medication. A lung transplant may be offered. Outcomes are often poor, with most people dying in months to years.
                            Definition sentence：Bronchiolitis obliterans (BO) is a lung disease characterized by inflammation and obstruction of the smallest airways (bronchioles), leading to symptoms like dry cough, shortness of breath, and fatigue, with progressive worsening over time.
                        """

NFCORPUS_LLM_QUERY_BASED_EXAMPLE = """
                            Query：Treatment for bronchiolitis obliterans
                            Definition sentence：Bronchiolitis obliterans (BO) is a lung disease characterized by inflammation and obstruction of the smallest airways (bronchioles), leading to symptoms like dry cough, shortness of breath, and fatigue, with progressive worsening over time.
                        """
