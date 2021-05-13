import pandas as pd

def process(number):
    df = pd.read_csv("user_csv"+str(number)+".csv", names=['user_id','country_code','user_name_len','full_name_len','intro_len','external_url','is_joined_recently','is_private','is_verified','is_business_account','highlight_reel_count','following_count','followed_count','post_count'])
    df = df[df.index%2==1]

    df2 = pd.read_csv("post_csv"+str(number)+".csv",usecols=[0,4,5,7,8,9],names=['user_id','comment_count','like_count','post_text_len','#_count','@_count'])
    length = len(df2)
    df2 = df2[df2.index%2==1]
    #user_id_list = []
    count = 1
    total_comment = 0
    total_like = 0
    total_post_len = 0
    total_sharp = 0
    total_at = 0

    external_url_list=[]

    avg_comment=[]
    avg_like=[]
    avg_post_len=[]
    avg_sharp=[]
    avg_at=[]

    var_comment=[]
    var_like=[]
    var_post_len=[]
    var_sharp=[]
    var_at=[]

    for url in df['external_url'].tolist():
        if(str(url)=='nan'):
            external_url_list.append(0)
        else:
            external_url_list.append(1)

    for userid in df['user_id'].tolist():
        if(df['post_count'][2*df['user_id'].tolist().index(userid)+1]=="0"):
            avg_comment.append(0)
            avg_like.append(0)
            avg_at.append(0)
            avg_post_len.append(0)
            avg_sharp.append(0)
            var_comment.append(0)
            var_like.append(0)
            var_at.append(0)
            var_post_len.append(0)
            var_sharp.append(0)
        elif(df['post_count'][2*df['user_id'].tolist().index(userid)+1]=="1"):
            if(df['is_private'][2*df['user_id'].tolist().index(userid)+1]=="False" or df['is_private'][2*df['user_id'].tolist().index(userid)+1]=="FALSE"):
                the_df = df2[df2['user_id']==userid]
                the_df['comment_count'] = the_df['comment_count'].astype(int)
                the_df['like_count'] = the_df['like_count'].astype(int)
                the_df['@_count'] = the_df['@_count'].astype(int)
                the_df['post_text_len'] = the_df['post_text_len'].astype(int)
                the_df['#_count'] = the_df['#_count'].astype(int)
                avg_comment.append(the_df['comment_count'].mean())
                avg_like.append(the_df['like_count'].mean())
                avg_at.append(the_df['@_count'].mean())
                avg_post_len.append(the_df['post_text_len'].mean())
                avg_sharp.append(the_df['#_count'].mean())
                var_comment.append(0)
                var_like.append(0)
                var_at.append(0)
                var_post_len.append(0)
                var_sharp.append(0)
            else:
                avg_comment.append(0)
                avg_like.append(0)
                avg_at.append(0)
                avg_post_len.append(0)
                avg_sharp.append(0)
                var_comment.append(0)
                var_like.append(0)
                var_at.append(0)
                var_post_len.append(0)
                var_sharp.append(0)
        else:
            if(df['is_private'][2*df['user_id'].tolist().index(userid)+1]=="False" or df['is_private'][2*df['user_id'].tolist().index(userid)+1]=="FALSE"):
                the_df = df2[df2['user_id']==userid]
                the_df['comment_count'] = the_df['comment_count'].astype(int)
                the_df['like_count'] = the_df['like_count'].astype(int)
                the_df['@_count'] = the_df['@_count'].astype(int)
                the_df['post_text_len'] = the_df['post_text_len'].astype(int)
                the_df['#_count'] = the_df['#_count'].astype(int)
                avg_comment.append(the_df['comment_count'].mean())
                avg_like.append(the_df['like_count'].mean())
                avg_at.append(the_df['@_count'].mean())
                avg_post_len.append(the_df['post_text_len'].mean())
                avg_sharp.append(the_df['#_count'].mean())
                var_comment.append(the_df['comment_count'].var())
                var_like.append(the_df['like_count'].var())
                var_at.append(the_df['@_count'].var())
                var_post_len.append(the_df['post_text_len'].var())
                var_sharp.append(the_df['#_count'].var())
            else:
                avg_comment.append(0)
                avg_like.append(0)
                avg_at.append(0)
                avg_post_len.append(0)
                avg_sharp.append(0)
                var_comment.append(0)
                var_like.append(0)
                var_at.append(0)
                var_post_len.append(0)
                var_sharp.append(0)

    is_joined_recently_list=[]
    is_private_list=[]
    is_verified_list=[]
    is_business_account_list=[]
    for a in df['is_joined_recently'].tolist():
        if a=="FALSE" or a=="False":
            is_joined_recently_list.append(0)
        else:
            is_joined_recently_list.append(1)

    for a in df['is_private'].tolist():
        if a=="FALSE" or a=="False":
            is_private_list.append(0)
        else:
            is_private_list.append(1)

    for a in df['is_verified'].tolist():
        if a=="FALSE" or a=="False":
            is_verified_list.append(0)
        else:
            is_verified_list.append(1)

    for a in df['is_business_account'].tolist():
        if a=="FALSE" or a=="False":
            is_business_account_list.append(0)
        else:
            is_business_account_list.append(1)

    data = {
            'user_id': df['user_id'],
            'country_code': df['country_code'],
            'user_name_len': df['user_name_len'],
            'full_name_len': df['full_name_len'],
            'intro_len': df['intro_len'],
            'external_url': external_url_list,
            # 'is_joined_recently':df['is_joined_recently'],
            # 'is_private':df['is_private'],
            # 'is_verified':df['is_verified'],
            # 'is_business_account':df['is_business_account'],
            'is_joined_recently':is_joined_recently_list,
            'is_private':is_private_list,
            'is_verified':is_verified_list,
            'is_business_account':is_business_account_list,
            'highlight_reel_count':df['highlight_reel_count'],
            'following_count': df['following_count'],
            'followed_count': df['followed_count'],
            'post_count': df['post_count'],
            'avg_comment': avg_comment,
            'avg_like': avg_like,
            'avg_post_len': avg_post_len,
            'avg_#':avg_sharp,
            'avg_@':avg_at,
            'var_comment':var_comment,
            'var_like':var_like,
            'var_post_len':var_post_len,
            'var_#':var_sharp,
            'var_@':var_at
        }     

    dataFrame = pd.DataFrame(data)
    dataFrame.to_csv("DataSet.csv",mode='a',header=False,index=False,sep=',')
