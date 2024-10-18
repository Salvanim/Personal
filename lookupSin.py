import math
WholeSin = [0.0,0.8414709848078965,0.9092974268256817,0.1411200080598672,-0.7568024953079282,-0.9589242746631385,-0.27941549819892586,0.6569865987187891,0.9893582466233818,0.4121184852417566,-0.5440211108893698,-0.9999902065507035,-0.5365729180004349,0.4201670368266409,0.9906073556948704,0.6502878401571168,-0.2879033166650653,-0.9613974918795568,-0.7509872467716762,0.14987720966295234,0.9129452507276277,0.8366556385360561,-0.008851309290403876,-0.8462204041751706,-0.9055783620066238,-0.13235175009777303,0.7625584504796027,0.956375928404503,0.27090578830786904,-0.6636338842129675,-0.9880316240928618,-0.404037645323065,0.5514266812416906,0.9999118601072672,0.5290826861200238,-0.428182669496151,-0.9917788534431158,-0.6435381333569995,0.2963685787093853,0.9637953862840878,0.7451131604793488,-0.158622668804709,-0.9165215479156338,-0.8317747426285983,0.017701925105413577,0.8509035245341184,0.9017883476488092,0.123573122745224,-0.7682546613236668,-0.9537526527594719,-0.26237485370392877,0.6702291758433747,0.9866275920404853,0.39592515018183416,-0.5587890488516163,-0.9997551733586199,-0.5215510020869119,0.43616475524782494,0.9928726480845371,0.6367380071391379,-0.3048106211022167,-0.9661177700083929,-0.7391806966492228,0.16735570030280691,0.9200260381967907,0.8268286794901034,-0.026551154023966794,-0.8555199789753223,-0.8979276806892913,-0.11478481378318722,0.7738906815578891,0.9510546532543747,0.25382336276203626,-0.6767719568873076,-0.9851462604682474,-0.38778163540943045,0.5661076368981803,0.9995201585807313,0.5139784559875352,-0.4441126687075084,-0.9938886539233752,-0.6298879942744539,0.31322878243308516,0.9683644611001854,0.7331903200732922,-0.1760756199485871,-0.9234584470040598,-0.8218178366308225,0.03539830273366068,0.8600694058124532,0.8939966636005579,0.10598751175115685,-0.7794660696158047,-0.9482821412699473,-0.24525198546765434,0.683261714736121,0.9835877454343449,0.3796077390275217,-0.5733818719904229,-0.9992068341863537,-0.5063656411097588,0.45202578717835057,0.9948267913584063,0.6229886314423488,-0.32162240316253093,-0.9705352835374847,-0.7271425000808526,0.18478174456066745,0.926818505417785,0.8167426066363169,-0.044242678085070965,-0.8645514486106083,-0.8899956043668333,-0.09718190589320902,0.7849803886813105,0.9454353340247703,0.23666139336428604,-0.689697940935389,-0.9819521690440836,-0.3714041014380902,0.5806111842123143,0.9988152247235795,0.4987131538963941,-0.45990349068959124,-0.9956869868891794,-0.6160404591886565,0.329990825673782,0.972630067242408,0.7210377105017316,-0.19347339203846847,-0.9301059501867618,-0.8116033871367005,0.05308358714605824,0.8689657562142357,0.8859248164599484,0.08836868610400143,-0.7904332067228887,-0.9425144545582509,-0.2280522595008612,0.6960801312247415,0.9802396594403116,0.363171365373259,-0.5877950071674065,-0.9983453608739179,-0.49102159389846933,0.4677451620451334,0.9964691731217737,0.6090440218832924,-0.3383333943242765,-0.9746486480944947,-0.7148764296291646,0.20214988141565363,0.933320523748862,0.8064005807754863,-0.06192033725605731,-0.8733119827746476,-0.8817846188147811,-0.0795485428747221,0.7958240965274552,0.9395197317131483,0.21942525837900473,-0.702407785577371,-0.9784503507933796,-0.35491017584493534,0.5949327780232085,0.9977972794498907,0.48329156372825655,-0.47555018687189876,-0.9971732887740798,-0.6019998676776046,0.3466494554970303,0.9765908679435658,0.7086591401823227,-0.2108105329134813,-0.9364619742512132,-0.8011345951780408,0.07075223608034517,0.8775897877771157,0.8775753358042688,0.07072216723899125,-0.8011526357338304,-0.936451400117644,-0.21078106590019152,0.7086804082392084,0.9765843832906294,0.346621180094276,-0.6020239375552833,-0.997171023392149,-0.47552366901205834,0.48331795366796265,0.9977992786806003,0.594908548461427,-0.3549383576518463,-0.9784565746221131,-0.7023863292684921,0.21945466799406363,0.9395300555699313,0.7958058429196471,-0.07957859166428352,-0.8817988360675502,-0.8732972972139946,-0.06189025071872073,0.8064184068658304,0.9333097001669604,0.2021203593127912,-0.7148975077677643,-0.97464190312541,-0.3383050275409778,0.6090679301910603,0.9964666417661079,0.46771851834275896,-0.491047853850463,-0.9983470937967718,-0.5877706198198406,0.36319945137636067,0.9802456219572225,0.6960584883449115,-0.22808160941352784,-0.9425245273294025,-0.7904147414931815,0.08839871248753149,0.8859387978787574,0.8689508382163493,0.05305348526993529,-0.8116209973649745,-0.9300948780045254,-0.19344381715900788,0.7210585970706318,0.9726230624856244,0.32996236973239734,-0.6160642040533645,-0.9956841897581032,-0.4598767232321427,0.49873928180328125,0.9988166912028082,0.5805866409896446,-0.37143208943692263,-0.9819578697820255,-0.6896761131802671,0.2366906812750767,0.9454451549211168,0.7849617132764033,-0.09721190751822432,-0.8900093488562771,-0.8645362993442719,-0.04421256322855966,0.8167599996228085,0.9268071855026884,0.184752119221718,-0.727163193443649,-0.9705280195418053,-0.3215938602925038,0.623012211003653,0.9948237286710673,0.45199889806298343,-0.5063916349244909,-0.9992080341070627,-0.5733571748155426,0.37963562682930313,0.9835931839466808,0.6832397038158508,-0.24528120908194284,-0.9482917095220488,-0.7794471854988634,0.10601748626711377,0.8940101700837942,0.8600540264645697,0.035368177256176046,-0.8218350110128397,-0.9234468802429867,-0.1760459464712114,0.7332108186087175,0.9683569384347241,0.3132001548706699,-0.6299114066849614,-0.9938853259197261,-0.4440856600409099,0.5140043136735694,0.99952109184891,0.5660827877060441,-0.3878094208292295,-0.9851514363288851,-0.6767497645263835,0.253852519790234,0.9510639681125854,0.7738715902084317,-0.11481475884166603,-0.8979409481081247,-0.8555043707508208,-0.026521020285755953,0.8268456339220814,0.9200142254959646,0.16732598101183924,-0.739200998751274,-0.9661099892625297,-0.30478191109030295,0.6367612505645516,0.992869055025318,0.43613762914604876,-0.5215767216183704,-0.9997558399011495,-0.5587640495890891,0.39595283104274065,0.9866325048439105,0.6702068037805061,-0.2624039418616639,-0.9537617134939987,-0.7682353642374471,0.12360303600011291,0.9018013749637745,0.8508876886558596,0.01767178546737087,-0.8317914757822045,-0.9165094902005468,-0.15859290602857282,0.7451332645574127,0.9637873480674221,0.2963397884973224,-0.6435612059762619,-0.9917749956098326,-0.42815542808445156,0.5291082654818533,0.9999122598719259,0.551401533867395,-0.4040652194563607,-0.9880362734541701,-0.6636113342009432,0.2709348053161655,0.9563847343054627,0.7625389491684939,-0.13238162920545193,-0.9055911481970673,-0.8462043418838515,-0.008821166113885877,0.8366721491002946,0.9129329489429682,0.14984740573347818,-0.7510071512506543,-0.9613891968218607,-0.2878744485084861,0.6503107401625525,0.9906032333897737,0.4201396822393068,-0.5365983551885637,-0.9999903395061709,-0.5439958173735323,0.412145950487085,0.9893626321783087,0.6569638725243396,-0.27944444178438205,-0.9589328250406132,-0.7567827912998033,0.14114985067939137,0.9093099708898409,0.8414546973619527,-3.014435335948845e-05,-0.8414872714892108,-0.9092848819352602,-0.14109016531210986,0.7568221986283603]
DecimalSin = [0.0,0.09983341664682815,0.19866933079506122,0.29552020666133955,0.3894183423086505,0.479425538604203,0.5646424733950354,0.644217687237691,0.7173560908995228,0.7833269096274834]

def sin(num):
    if str(num).__contains__('.'):
        splitFromDecimal = str(num).split('.')
        wholeNumSin = WholeSin[(int(splitFromDecimal[0]))%360]
        # otherDigits = list(map(int, list(splitFromDecimal[1])))
        # sumTotal = 0
        # placeDigit = 10
        # for d in otherDigits:
        #     sumTotal += WholeSin[d]
        #     placeDigit *= 10
        return wholeNumSin, WholeSin[int(splitFromDecimal[1])%360]
    else:
        return WholeSin[num%360]

print(sin(float(input("Number: "))))