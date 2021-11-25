# %%
base_url = 'https://www.ryanscomputers.com/search?q='
qry = input('Which product are you finding? - ')
p_qry1 = qry.strip().replace(' ', '+')
p_qry2 = qry.strip().replace(' ', '%20')
idx = '&idx=products&p='
page_counter = 0
search_url = base_url + p_qry1
print(search_url)


# %%
