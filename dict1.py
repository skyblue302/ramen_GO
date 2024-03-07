#拉麵資訊列表


ramen_list = ['隱家拉麵',\
            '雞吉君',\
            '麵屋武藏',\
            '麵屋昕家',\
            '麵屋一燈',\
            '勝王',\
            '鳥人拉麵',\
            '鬼金棒',\
            '鷹流蘭丸',\
            '柑橘',\
            '墨洋拉麵',\
            '道樂拉麵',\
            '博多拉麵',\
            '一幻拉麵',\
            '樂麵屋',\
            '藏味拉麵',\
            '真劍拉麵',\
            '長生塩人',\
            '麵屋壹慶',\
            '山嵐拉麵',\
            '五之神製作所',\
            '拉麵公子',\
            '特濃屋',\
            '壹之穴沾麵',\
            '一蘭',\
            '麵試十一次'\
            '一風堂']

#分店抽取


ramen_link_dict = {'隱家拉麵_士林店':'https://goo.gl/maps/qoAmJ7qC44CFuq227',\
                   '隱家拉麵_芝山店':'https://goo.gl/maps/72LVPZTSpPhfJP616',\
                   '隱家拉麵_赤峰店':'https://goo.gl/maps/vqf1ftXKyMfuN36Q8',\
                   '隱家拉麵_公館店':'https://goo.gl/maps/Qd9r7yRJybWkhhzx6',\
                   '雞吉君':'https://goo.gl/maps/P2dRLkg1hVrpXoT68',\
                   '麵屋武藏_神山':'https://goo.gl/maps/AQHGhubyxZEwfVmP9',\
                   '麵屋武藏_本店':'https://goo.gl/maps/aJvG2PFabJZtAHJq5',\
                   '麵屋昕家':'https://goo.gl/maps/SSmX7C41PB38Yax28',\
                   '麵屋一燈':'https://g.page/menyaittotw?share',\
                   '勝王':'https://g.page/ramenkatsuo?share',\
                   '鳥人拉麵_台灣總店':'https://goo.gl/maps/AtvQYEZAVmJMB48u6',\
                   '鳥人拉麵_中山店':'https://goo.gl/maps/jkdmDXJRMQpaoTZ2A',\
                   '鳥人拉麵_西門店':'https://goo.gl/maps/aNgbiy36AevYv8FG7',\
                   '鬼金棒味噌拉麵_台北本店':'https://goo.gl/maps/CZouik7WCkxUa3zEA',\
                   '鬼金棒味噌沾麵_台北本店':'https://goo.gl/maps/oczfkWKSHjotLpp37',\
                   '鬼金棒_松江南京':'https://goo.gl/maps/g6WrUCZy3cMRUNG29',\
                   '鷹流蘭丸_中山店':'https://goo.gl/maps/KrtudHkVHKhyfboD8',\
                   '柑橘_Soba':'https://g.page/citrusshinnsoba?share',\
                   '柑橘_鴨蔥':'https://g.page/citrusshinnduckramen?share',\
                   '柑橘_魚水':'https://goo.gl/maps/Q4ScRVAuFExQP9wy8',\
                   '墨洋拉麵':'https://goo.gl/maps/2M7M9CibGp7THPXG9',\
                   '道樂屋台':'https://goo.gl/maps/Qf3dn28DDSgkqsik9',\
                   '道樂拉麵_大北店':'https://goo.gl/maps/iB7fidksSEYjD95CA',\
                   '道樂商店':'https://goo.gl/maps/GH9p7YPUGktrhYFDA',\
                   '博多拉麵_台灣總店':'https://goo.gl/maps/hzkRKHMk91cddRsJ7',\
                   '博多拉麵_市大店':'https://goo.gl/maps/X8VFXQRSgNsEPc788',\
                   '一幻拉麵_台北信義店':'https://goo.gl/maps/9A3vPrS1PqzsLxQ39',\
                   '樂麵屋_永康店':'https://goo.gl/maps/6vMJzh6bdw7dk1uz8',\
                   '樂麵屋_永康公園店':'https://goo.gl/maps/AzQX675U6a2oE2KT6',\
                   '樂麵屋_西門店':'https://goo.gl/maps/BWZCt4qBxNxyUoYR6',\
                   '樂麵屋_南港店':'https://goo.gl/maps/37a6Gq1qU6yPCCws5',\
                   '藏味拉麵':'https://goo.gl/maps/wUMxbuVwddzWW5Bu5',\
                   '真劍拉麵':'https://goo.gl/maps/evSjwNQGWDAi17tcA',\
                   '長生塩人_天母':'https://goo.gl/maps/5W6iLtZETomxWJ377',\
                   '長生塩人_辛亥':'https://goo.gl/maps/PgKtgzsf8ZBBfm199',\
                   '長生塩人_民生':'https://goo.gl/maps/QzWPwBBze4DMn3H88',\
                   '長生塩人_北投車站':'https://goo.gl/maps/goeK56EwcbEd7qk39',\
                   '麵屋壹慶':'https://goo.gl/maps/tWiWiLX1zLRnUxKJ7',\
                   '山嵐拉麵_大安店':'https://goo.gl/maps/kLeLopT6GaNPg7aG7',\
                   '山嵐拉麵_古亭店':'https://goo.gl/maps/Z6Ra75kTxm6Xdu9k8',\
                   '山嵐拉麵_公館店':'https://goo.gl/maps/Qrk33FnuubdT8LFF6',\
                   '山嵐拉麵_林森八條店':'https://goo.gl/maps/ox3MFs8VwCNL6Q8Z6',\
                   '五之神製作所':'https://goo.gl/maps/zyJMXwDXYRqs3wTVA',\
                   '拉麵公子':'https://goo.gl/maps/LZ1ynFdETPT7C9sy7',\
                   '特濃屋':'https://goo.gl/maps/cuP2XejD3cB4penu7',\
                   '壹之穴沾麵':'https://goo.gl/maps/1PFKuefntjxxayFe9',\
                   '一蘭_台灣台北本店':'https://g.page/ichiran-tw?share',\
                   '一蘭_台灣台北別館':'https://g.page/ichiran-tw2?share',\
                   '麵試十一次':'https://g.page/noodles11?share',\
                   '一風堂_中山本店':'https://goo.gl/maps/bQq63hrjqNgkYMqt9',\
                   '一風堂_微風北車店':'https://goo.gl/maps/geYZZYkeS1PBNQWx6',\
                   '一風堂_台北101店':'https://goo.gl/maps/rySKaALdtgywxuTC7',\
                   '一風堂_微風南山店':'https://g.page/ippudo4011?share',\
                   '一風堂_新莊宏匯店':'https://goo.gl/maps/pdpqgaxipZaYeXMN8',\
                   }


