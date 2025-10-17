

import parse_utils


class QuerySeveral:
    word_freq_dict = {} # the dictionary of words to dict of ids to counts
    id_title_dict = {}  # the dictionary of ids to titles

    
    def __init__(self, wikifile):
        parse_utils.parse(wikifile, self.process_page)
    

    def process_page(self, wiki_page:str):
        """
        reads one wiki/xml file, processes each page, populating the
        dictionary that maps words->page_id->frequency counts
        
        parameters:
            wiki_page   the path to an xml file with pages (each with title, 
                        id, and text sections)
        """
        
        page_id = int(wiki_page.find("id").text)
        page_title = wiki_page.find("title").text.strip()
        page_text = wiki_page.find("text").text.strip()
        if wiki_page.find("text").text is None: page_text = ""
        
        self.id_title_dict[page_id] = page_title

        tokens = parse_utils.get_tokens(page_title + " " + page_text)
        
        for word in tokens:
            if parse_utils.word_is_link(word):
                # split link into the text and the destination, but only process the text
                # TODO: Fill in!
                link_words, _ = parse_utils.split_link(word)
                # include link text because it's part of the page text
                for link_word in link_words:
                    self._update_word_freq(link_word.lower(), page_id)
                # TODO: Fill in!
    
            else:
                # for non-links, just record its presence
                self._update_word_freq(word.lower(), page_id)
                # TODO: Fill in!
                
        

    def query(self, search_term:str, format="title") -> list:
        """
        searches for page titles that contain the search term

        Parameters:
        search_term -- the string to search for in wiki pages; for this
                       assignment these can be just single words

        format -- used to control whether a list of page ids or titles 
                  is returned. title is the default, but the value can
                  be set to "id" when query is called to get the page 
                  ids instead (ids might be less error-prone to check in tests)
        
        Returns:
        the list of pages that contain the search term (as per the format)
        """
        if format not in ["id", "title"]:
            raise ValueError("Invalid results format " + format)
        
        term_low = search_term.lower()
        if term_low in parse_utils.STOP_WORDS:
            print("WARNING: STOP WORD isn't indexed -- " + search_term)
            return []

        term_low = parse_utils.stem_and_stop(term_low)
        if term_low in self.word_freq_dict:
            # if the term is in the dictionary, get the list of ids and sort it
            # TODO: Fill in!
            # sort the pairs by frequency
            page_freqs = self.word_freq_dict[term_low].items()
            sorted_pages = sorted(page_freqs, key=lambda x: (-x[1], x[0]))
            results = [page_id for page_id, _ in sorted_pages]
            
            if format=="id": 
                # TODO: Fill in!
                #just return ids
                return results
                
            elif format=="title": 
                # TODO: Fill in!
                #iterate through to get title of each id
                return [self.id_title_dict[page_id] for page_id in results]
            
        else:
            return []


    def _update_word_freq(self, word: str, page_id: int):
        """
        Updates the word frequency dictionary for the given word and page_id.

        Parameters:
            word    -- the word to update
            page_id -- the page id of the page where the word occurred
        """
        # skip if the word is a stop word
        if word in parse_utils.STOP_WORDS:
            return
        
        # Apply stemming and stop word removal
        word = parse_utils.stem_and_stop(word)
        if word == "":  # if empty, skip
            return

        # add to dict if not already there
        if word not in self.word_freq_dict:
            self.word_freq_dict[word] = {}
        if page_id not in self.word_freq_dict[word]:
            self.word_freq_dict[word][page_id] = 0

        self.word_freq_dict[word][page_id] += 1  

