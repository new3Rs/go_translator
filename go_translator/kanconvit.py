# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
"""
kanconvit.jsのPythonへの移植
簡体字の代用字は変換を抑制するように仕様を変更しています。
Python3にて動作確認。
作者: 市川雄二
日付: 2017/09/29
ソース: http://blog.livedoor.jp/dankogai/archives/51224227.html
"""
import re

_zh = \
    '丑专业丛东丝丢两严丧个丰临为丽举么义乌乐乔乘习乡书买亏云亚产亩亲' + \
    '亿仅仆从仑仓仪们价仿众优伙伞伟传伤伦伪佛你佣侠侣侥侦侧侨俩俭债值' + \
    '倾假偿储儿兑兰关兴养兽冈册军农冯冰冲决况冻净凄凉凌减凑凛几凤凭凯' + \
    '击凿划刘则刚创删别刽剂剑剥剧剩劝办务动劲劳势勋匀华协单卖卜卢卤卧' + \
    '卫卷厂厅历厉压厌厕厢厦厨县叁发变叠只叶叹吁吃吊后吓吕吗吨听启吴呕' + \
    '员呛呜咏咙咸响哑哗哟唤啰啸喷嚣团园囱围图圆圈圣场坏块坚坛坝坞坟坠' + \
    '垄垒垦垫墙增壤壳壶壹处备复够头夸夹夺奋奖妆妇妈姊娄娇娘娱婴婶孙宁' + \
    '实宠审宪宫宽宾对寻导尔尘尝尸层屉屡屿岁岂岗岛岭峦崭巢巩币帅师帐帘' + \
    '帜带帮并广庄庆庐库应庙庞废开异弃张弥弯弹强归录彻德忆忧怀态怜总恳' + \
    '恶恼悬悯惊惠惧惩惫惭惯愈愤愿懒戏战户扎扑托执扩扫扬扰抚抠抡抢护报' + \
    '抬拂拔拜拟拢拣拥拦拧拨择挂挚挠挡挣挤挥捞损捡换捣据捻掷掸掺插揭揽' + \
    '搀搁搂搅搜摄摆摇摊撑撵攒收效敌敛斋斩无时旷昙显晋晒晓晕晚暂术朴机' + \
    '杀杂权杨杰极构枣枪枫柜柠查栅标栈栋栏树栖样档桥桨桩梦检椭榨樱橱欢' + \
    '步歼毁每毕毙毡气氛氢汇汉污汤汹沉沟沥沦沧沪泞泪泻泼泽洁洒洼浆浇浊' + \
    '测济浑浓涂涉涌涛涝涡涣涤润涧涨涩淀渊渐渔渗渴游溃溅溪滚满滤滥滨滩' + \
    '澜濒灭灵灶灾灿炮炼烁烂烛烟烦烧烫热焕爱爷牵牺犹狈狞狮狰狱猎猪玛环' + \
    '现琐琼瓮电畅畴疏疗疟疮疯痒痪瘪瘫癣皱盏盐监盖盘睁瞒矫矾矿码砖砚砾' + \
    '础硅硕确碍碎碱祷祸离秃秆种积秸秽稳稻穗穷窍窑窗窜窝窥竖竞笋笔笼筑' + \
    '筛筹签简箩篓篮篱类粤粪粮粹紧纠红纤约级纪纫纬纯纱纲纳纵纷纸纹纺纽' + \
    '线练组绅细织终绊绍绎经绑绒结绕绘给络绝绞统绢绣继绩绪续绰绳维绵绷' + \
    '绸综绽绿缀缅缆缎缓缔缕编缘缚缝缠缨缩缴网罗罚罢羡翘耸耻聂聋职联聪' + \
    '肃肠肤肾肿胀胁胜胶脉脏脐脑脓脸腊腻腾舆舍舰舱艰艳艺节芜芦苇苍苏苹' + \
    '范茧荆荐荚荡荣荤荧药莱莲获莹萝萤营萧萨葱蒋蓝蔼蕴藏虏虑虽虾蚀蚁蚂' + \
    '蜕蜗蜡蝇蝉蝎衅衔补衬袄袜袭裤裹见观规觅视览觉誊计订认讥讨让训议讯' + \
    '记讲讳讶许讹论讼讽设访诀证评诅识诈诉诊词译试诗诚话诞诡询该详诫诬' + \
    '语误诱诲说诵请诸诺读诽课谁调谅谆谈谊谋谍谎谐谒谓谚谜谢谣谤谦谨谬' + \
    '谭谱谴谷贝贞负贡财责贤败账货质贩贪贫贬购贮贯贰贱贴贵贷贸费贺贼贾' + \
    '贿赁赂赃资赊赋赌赎赏赐赔赖赘赚赛赞赠赡赢赵赶趋跃踪躯车轧轨轩转轮' + \
    '软轰轴轻载轿较辅辆辈辉辐辑输辕辖辙辩辫边辽达迁过迈运还这进远违连' + \
    '迟迹适选逊递逻遗遥邓邮邻郑酝酱酿醉采释鉴针钉钓钙钝钞钟钠钢钥钦钧' + \
    '钩钮钱钳钻钾铁铃铅铆铜铝铡铣铭铲银铸铺链销锁锄锅锈锋锌锐错锚锡锣' + \
    '锤锥锦锨锭键锯锰锹锻镀镇镊镐镜镣镰镶长门闪闭问闯闰闲间闷闸闹闺闻' + \
    '闽阀阁阅阎阐阔队阳阴阵阶际陆陈陕陨险陷隐隶难雏雕雾霉霸韧韩韵页顶' + \
    '顷项顺须顽顾顿颁颂预颅领颇颈颊频颓颖颗题颜额颠颤风飘飞饥饭饮饰饱' + \
    '饲饵饶饺饼饿馁馅馆馋馏馒马驮驯驰驱驳驴驶驹驻驼驾骂骄骆骇验骏骑骗' + \
    '骚骡骤髓鱼鲁鲜鲤鲸鳖鳞鸟鸡鸣鸥鸦鸭鸯鸳鸵鸽鸿鹃鹅鹊鹏鹤鹰黑默齐齿' + \
    '龄龙龟' + \
    '真谞笃龙'

_ja = \
    '醜専業叢東絲丟両厳喪個豊臨為麗挙麽義烏楽喬乗習郷書買虧雲亜産畝親' + \
    '億僅僕従侖倉儀們価倣衆優夥傘偉伝傷倫偽仏妳傭俠侶僥偵側僑倆倹債値' + \
    '傾仮償儲児兌蘭関興養獣岡冊軍農馮氷沖決況凍浄淒涼淩減湊凜幾鳳憑凱' + \
    '撃鑿劃劉則剛創刪別劊剤剣剝劇剰勧辦務働勁労勢勲勻華協単売蔔盧鹵臥' + \
    '衛巻廠庁暦厲圧厭廁廂廈廚県三発変畳隻葉嘆籲喫弔後嚇呂嗎噸聴啓呉嘔' + \
    '員嗆嗚詠嚨鹹響啞嘩喲喚啰嘯噴囂団園囪囲図円圏聖場壊塊堅壇壩塢墳墜' + \
    '壟塁墾墊牆増壌殻壺壱処備復夠頭誇夾奪奮奨粧婦媽姉婁嬌嬢娯嬰嬸孫寧' + \
    '実寵審憲宮寛賓対尋導爾塵嘗屍層屜屢嶼歳豈崗島嶺巒嶄巣鞏幣帥師帳簾' + \
    '幟帯幫併広荘慶廬庫応廟龐廃開異棄張彌彎弾強帰録徹徳憶憂懐態憐総懇' + \
    '悪悩懸憫驚恵懼懲憊慚慣癒憤願懶戯戦戸紮撲託執拡掃揚擾撫摳掄搶護報' + \
    '擡払抜拝擬攏揀擁攔擰撥択掛摯撓擋掙擠揮撈損撿換搗拠撚擲撣摻挿掲攬' + \
    '攙擱摟攪捜摂擺揺攤撐攆攢収効敵斂斎斬無時曠曇顕晉曬暁暈晩暫術樸機' + \
    '殺雑権楊傑極構棗槍楓櫃檸査柵標桟棟欄樹棲様檔橋槳樁夢検橢搾桜櫥歓' + \
    '歩殲毀毎畢斃氈気雰氫彙漢汚湯洶沈溝瀝淪滄滬濘涙潟潑沢潔灑窪漿澆濁' + \
    '測済渾濃塗渉湧濤澇渦渙滌潤澗漲渋澱淵漸漁滲渇遊潰濺渓滾満濾濫濱灘' + \
    '瀾瀕滅霊竈災燦砲錬爍爛燭煙煩焼燙熱煥愛爺牽犠猶狽獰獅猙獄猟豬瑪環' + \
    '現瑣瓊甕電暢疇疎療瘧瘡瘋癢瘓癟癱癬皺盞塩監蓋盤睜瞞矯礬鉱碼磚硯礫' + \
    '礎矽碩確礙砕堿禱禍離禿稈種積稭穢穏稲穂窮竅窯窓竄窩窺豎競筍筆籠築' + \
    '篩籌簽簡籮簍籃籬類粵糞糧粋緊糾紅繊約級紀紉緯純紗綱納縦紛紙紋紡紐' + \
    '線練組紳細織終絆紹繹経綁絨結繞絵給絡絶絞統絹繡継績緒続綽縄維綿繃' + \
    '綢綜綻緑綴緬纜緞緩締縷編縁縛縫纏纓縮繳網羅罰罷羨翹聳恥聶聾職聯聡' + \
    '粛腸膚腎腫脹脅勝膠脈臓臍脳膿臉臘膩騰輿舎艦艙艱豔芸節蕪蘆葦蒼蘇蘋' + \
    '範繭荊薦莢蕩栄葷熒薬萊蓮獲瑩蘿蛍営蕭薩蔥蔣藍藹蘊蔵虜慮雖蝦蝕蟻螞' + \
    '蛻蝸蠟蠅蟬蠍釁銜補襯襖襪襲褲裏見観規覓視覧覚謄計訂認譏討譲訓議訊' + \
    '記講諱訝許訛論訟諷設訪訣証評詛識詐訴診詞訳試詩誠話誕詭詢該詳誡誣' + \
    '語誤誘誨説誦請諸諾読誹課誰調諒諄談誼謀諜謊諧謁謂諺謎謝謡謗謙謹謬' + \
    '譚譜譴穀貝貞負貢財責賢敗賬貨質販貪貧貶購貯貫弐賤貼貴貸貿費賀賊賈' + \
    '賄賃賂贓資賒賦賭贖賞賜賠頼贅賺賽賛贈贍贏趙趕趨躍蹤軀車軋軌軒転輪' + \
    '軟轟軸軽載轎較輔輛輩輝輻輯輸轅轄轍弁弁辺遼達遷過邁運還這進遠違連' + \
    '遅跡適選遜逓邏遺遙鄧郵隣鄭醞醬醸酔採釈鑑針釘釣鈣鈍鈔鐘鈉鋼鑰欽鈞' + \
    '鈎鈕銭鉗鑽鉀鉄鈴鉛鉚銅鋁鍘銑銘鏟銀鋳舗鏈銷鎖鋤鍋鏽鋒鋅鋭錯錨錫鑼' + \
    '錘錐錦鍁錠鍵鋸錳鍬鍛鍍鎮鑷鎬鏡鐐鐮鑲長門閃閉問闖閏閑間悶閘鬧閨聞' + \
    '閩閥閣閲閻闡闊隊陽陰陣階際陸陳陝隕険陥隠隷難雛彫霧黴覇韌韓韻頁頂' + \
    '頃項順須頑顧頓頒頌預顱領頗頸頰頻頹穎顆題顔額顛顫風飄飛飢飯飲飾飽' + \
    '飼餌饒餃餅餓餒餡館饞餾饅馬駄馴馳駆駁驢駛駒駐駝駕罵驕駱駭験駿騎騙' + \
    '騒騾驟髄魚魯鮮鯉鯨鼈鱗鳥鶏鳴鷗鴉鴨鴦鴛鴕鴿鴻鵑鵝鵲鵬鶴鷹黒黙斉歯' + \
    '齢竜龜' + \
    '眞諝篤龍'

_sound_alternatives = '丑干谷后斗'
_numbers = '〇一二三四五六七八九十'

_re_zh = re.compile('[' + _zh + ']')
_re_ja = re.compile('[' + _ja + ']')
_zh2ja = {}
_ja2zh = {}

for i in range(len(_zh)):
    _zh2ja[_zh[i]] = _ja[i]
    _ja2zh[_ja[i]] = _zh[i]

def zh2ja(string):
    return _re_zh.sub(lambda m: m.group(0) if m.group(0) in _sound_alternatives else _zh2ja[m.group(0)], string)

def ja2zh(string):
    return _re_ja.sub(lambda m: m.group(0) if m.group(0) in _numbers else _ja2zh[m.group(0)], string)

if __name__ == '__main__':
    print(zh2ja("烂柯"))
    print(ja2zh("高尾紳路"))
    print(ja2zh("羽根直樹"))
