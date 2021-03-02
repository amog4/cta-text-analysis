from common_text_functions import *
from nltk.corpus import stopwords
import config
import os 
#import argparse


#parser = argparse.ArgumentParser(description='Get the required paths and process commands')





def main(*args,**kwargs):

    modified_platform = file_path(path=str(directory))


    df = simple_read(modified_platform,
                                file_name = file_name,
                                file_type = file_type,
                                sheet_name=sheet_name,
                                enc=enc)


    _df  = df.copy()


    _df['clean_text']  = _df[column_name].apply(lambda x : re.sub("[^\x00-\x7f]",'',str(x)) )

    _df['clean_text']  = _df['clean_text'].apply(lambda x : x.replace('\n','') )

    _df['clean_text']  = _df['clean_text'].apply(lambda x : re.sub("[^a-zA-Z0-9@#$%^&*() -]",'', str(x)))

    stop = set(stopwords.words('english'))
    stop.add('')

    _df = wordtokenize(sentence =None,type = 'df',df = _df,column = 'clean_text',lower=True)

    _df = stop_words(type = 'df',stop = stop,sentence =None,df =_df ,column = 'words_tokenzie',sentence_type='list')


    word_frq = word_frequency_df(_df , column = 'stop_words_removed')

    bi_tri_frq = bigram_trigram(df = _df,column='stop_words_removed',bigram=True,trigram=True)

    bi_frq = word_frequency_df(bi_tri_frq , column = 'bi_grams')
    tri_frq = word_frequency_df(bi_tri_frq , column = 'tri_grams')
    _df.to_csv(stored_filepath+'df'+'_'+filename_to_save,index=False)
    
    word_frq.to_csv(stored_filepath+'word_frequency'+'_'+filename_to_save,index=False)
    bi_frq.to_csv(stored_filepath+'bi_frequency'+'_'+filename_to_save,index=False)
    tri_frq.to_csv(stored_filepath+'tri_frequency'+'_'+filename_to_save,index=False)

    del _df,word_frq,bi_tri_frq,bi_frq,tri_frq,df


if __name__ == "__main__":
    

    conf = config.conf['config']


    directory = conf['path']
    mk_dir(directory = directory)
    file_name = conf['file_name']
    file_type = conf['file_type']
    sheet_name = conf['sheet_name']
    enc  = conf['enc']
    column_name  = conf['column_name']
    stored_filepath  = conf['stored_filepath']
    mk_dir(directory =stored_filepath)
    filename_to_save = conf['filename_to_save']


    #main()