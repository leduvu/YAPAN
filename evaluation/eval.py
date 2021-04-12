"""
Le Duyen Sandra Vu
run: python3 eval.py
01.04.2021
"""


import nltk
from janome.tokenizer import Tokenizer

import re

import pandas as pd
df = pd.read_csv ('grammar.csv')


t = Tokenizer()

def tokenize(sentence):
	tagged = []


	for idx, token in enumerate(t.tokenize(sentence)):
		pos = ''
		pos1 = token.part_of_speech.split(',')[0]
		pos2 = ''
		if len(token.part_of_speech.split(',')) > 1:
			pos2 = token.part_of_speech.split(',')[1]
		if pos1 == '助詞':
			pos = 'PARTICLE'
		if pos1 == '名詞':
			pos = 'NOUN'
		if pos2 == '副詞可能':
			pos = 'ADV:NOUN'
		if pos1 == '形容詞' or token.infl_type == '形容詞・イ段':
			if token.infl_form == '基本形':
				# ookii
				pos = 'ADJ-Idict'
			else:
				# ooki
				pos = 'ADJ-I'
		if pos2 == '形容動詞語幹':
			pos = 'ADJ-NA'
		if pos1 == '動詞'  and token.infl_form in ['連用形', '連用タ接続']:
			pos = 'Vconj'
		if pos1 == '動詞' and token.infl_form == '基本形':
			pos = 'Vdict'
		if pos1 == '動詞' and token.infl_form == '命令ｒｏ':
			pos = 'Vimp'
		if pos1 == '動詞' and token.infl_form == '連用形':
			pos = 'Vstem1'
		if pos1 == '動詞' and token.infl_form == '連用形' and token.infl_type in ['一段', 'サ変・スル', '五段・サ行', 'カ変・来ル']:
			pos = 'Vstem12'
		if pos1 == '動詞' and token.infl_form == '連用タ接続':
			pos = 'Vstem2'
		if pos1 == '動詞' and token.infl_form == '仮定形':
			pos = 'Vba'
		if pos1 == '動詞' and token.infl_form == '未然ウ接続':
			pos = 'Vjo'
		if pos1 == '動詞' and token.infl_form == '未然形':
			pos = 'Vindef'
		if pos1 == '副詞':
			pos = 'ADV'
		if pos1 =='助動詞' and token.base_form in ['た', 'だ'] and token.surface != 'な':
			pos = 'TA'
			if token.surface == 'たら':
				pos = 'TARA'
			if token.surface == 'なら':
				pos = "NARA"
			if token.surface == 'で':
				pos = "DE"
		if pos1 =='助動詞' and token.infl_type == '特殊・ナイ':
			pos = 'NAI'
		if pos1 == '助詞' and (token.base_form == 'て' or token.base_form == 'で'):
			pos = 'TE'
		if pos1 == '助動詞' and token.base_form == 'ます':
			pos = 'MASU'
		if pos1 == '助動詞' and token.base_form == 'ん':
			pos = 'SEN'
		if pos1 == '助動詞' and token.base_form == 'です':
			pos = 'DESU'

		if pos == '':
			pos = pos1

		pos = token.surface + ':' + pos
		text = token.surface
		tagged.append((text,pos))
	return tagged


grammar = ('''
	SAIWAI_NA_KOTO_NI: {<幸い:.*><な:.*><こと:.*><に:.*>}
	SAIWAI_NA_KOTO_NI: {<幸い:ADV>}
 	TO_IU_KOTO_WA: {<という:.*><こと:.*><は:.*>}
	KOTO-YARA: {<こと:.*><やら:.*>}
    KOTO_WA_NAI: {<.*:Vdict><こと:.*><は:.*><ない:.*>}
    KOTO_NAKU: {<.*:Vdict><こと:.*><なく:.*>}
    KOTO_NI: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><こと:.*><に:.*>}
    KOTO_NI: {<.*:ADJ-Idict><こと:.*><に:.*>}
    KOTO_NI: {<.*:ADJ-NA><な:.*><こと:.*><に:.*>}
	KOTO_DA: {<.*:Vdict><こと:.*><です:.*|だ:.*|でした:.*>}
	KOTO_DA: {<.*:Vindef><ない:.*><こと:.*><です:.*|だ:.*|でした:.*>}
	KOTO_DA: {<.*:Vdict><こと:.*><だっ.*><た:.*>}
	KOTO_DA: {<.*:Vindef><ない:.*><こと:.*><だっ:.*><た:.*>}
    KOTO_NASHI_NI: {<こと:.*><なし:.*><に:.*>}
	NP-KOTO1pres: {<.*:Vdict><.*:Vdict><こと:.*>}
	NP-KOTO1: {<.*:Vstem1|.*:Vstem12><.*:NAI><.*:TA>?<こと:.*>}
	NP-KOTO1: {<.*:Vstem1|.*:Vstem12><.*:NAI><.*:TA>?<こと:.*>}
 	NP-O/GO_: {<お:.*|ご:.*><.*:NOUN|.*:ADJ-.*>}

	NP-CHUU/JUU_: {<.*NOUN><中:.*>}
	NP-GACHI_: {<.*NOUN><がち:.*>}
	NP-GACHI_: {<.*:Vstem1|.*:Vstem12><がち:.*>}
	NP-GIMI_: {<.*NOUN><気味:.*|ぎみ:.*>}
	NP-GIMI_: {<.*:Vstem1|.*:Vstem12><気味:.*|ぎみ:.*>}
	NP-KOSO_: {<こそ:.*><.*NOUN>}
	NP-MUKE_: {<.*NOUN><向け:.*|むけ:.*>}
	NP-MUKI_: {<.*NOUN><向き:.*|むき:.*>}
 	NP-SA_: {<.*:ADJ-NA|.*ADJ-I><さ:.*>}

 	NP-AGEKU: {<あげく:.*NOUN>}
 	NP-AMARI: {<あまり:.*NOUN>}
 	NP-AIDA: {<間:.*NOUN>}
	NP-ATO: {<後:.*NOUN|あと:.*NOUN>}
	NP-BA: {<ば:.*NOUN>}
	NP-BAAI: {<場合:.*NOUN>}
	NP-BETSU: {<別:.*NOUN>}
	NP-BURI: {<ぶり:.*NOUN>}
	NP-CHIGAI: {<違い:.*NOUN>}
	NP-CHUUSHIN: {<中心:.*NOUN>}
	NP-DOKORO: {<どころ:.*NOUN>}
	NP-DOORI: {<どおり:.*NOUN>}
	NP-FUU: {<ふう:.*NOUN|風:.*NOUN>}
	NP-FURI: {<ふり:.*>}
	NP-GE: {<げ:.*>}
	NP-GORAN: {<ごらん:.*NOUN>}
	NP-GOTO: {<ごと:.*NOUN>}
	NP-GURUMI: {<ぐるみ:.*NOUN>}
	NP-HAJIME: {<はじめ:.*NOUN>}
	NP-HAME: {<羽目:.*NOUN>}
	NP-HAZU: {<はず:.*NOUN>}
	NP-HOKA: {<ほか:.*NOUN>}
	NP-HOU: {<方:.*NOUN|ほう:.*NOUN>}
	NP-HYOUSHI: {<拍子:.*NOUN>}
	NP-ICHIBAN: {<一番:.*NOUN|いちばん:.*NOUN>}
	NP-IGAI: {<以外:.*NOUN>}
	NP-IJOU: {<以上:.*NOUN>}
	NP-IKAN: {<いかん:.*NOUN>}
	NP-INA: {<否:.*NOUN>}
	NP-ITARI: {<至り:.*NOUN>}
	NP-IPPOU: {<一方:.*NOUN>}
	NP-IRAI: {<以来:.*NOUN>}
	NP-IZURE: {<いずれ:.*NOUN>}
	NP-JIMAI: {<じまい:.*NOUN>}
	NP-KAI: {<かい:.*NOUN|甲斐:.*NOUN>}
	NP-KATAGATA: {<かたがた:.*NOUN>}
	NP-KATAWARA: {<かたわら:.*NOUN>}
	NP-KAGIRI: {<限り:.*NOUN>}
	NP-KAWARI: {<代わり:.*NOUN>}
	NP-KAWAKIRI: {<皮切り:.*NOUN>}
	NP-KEIKI: {<契機:.*NOUN>}
	NP-KEKKA: {<結果:.*NOUN|けっか:.*NOUN>}
	NP-KI:{<機:.*NOUN>}
	NP-KIRI: {<きり:.*NOUN|っきり:.*NOUN>}
	NP-KIWAMI: {<極み:.*NOUN>}
	NP-KORO: {<ころ:.*NOUN>}
	NP-KOTO: {<こと:.*NOUN>}
	NP-KUSE: {<くせ:.*NOUN>}
	NP-MAE: {<前:.*NOUN>}
	NP-MAMA: {<まま:.*NOUN>}
	NP-MAMIRE: {<まみれ:.*NOUN>}
	NP-MITAI: {<みたい:.*NOUN>}
	NP-MON: {<もん:.*NOUN>}
	NP-MONO: {<もの:.*NOUN>}
	NP-MOTO: {<もと:.*NOUN>}
	NP-NAMI: {<並み:.*NOUN>}
	NP-NANI: {<何:.*NOUN|なに:.*NOUN>}
	NP-NAN: {<なん:.*NOUN>}
	NP-NARADEWA: {<ならでは:.*NOUN>}
	NP-NAKA: {<中:.*NOUN|なか:NOUN>}
	NP-N: {<ん:.*NOUN>}
	NP-NO: {<の:.*NOUN>}
	NP-NUKI: {<抜き:.*NOUN>}
	NP-OKAGE: {<おかげ:.*NOUN>}
	NP-OKI: {<おき:.*NOUN>}
	NP-OMAKE: {<おまけ:.*NOUN>}
	NP-OROKA: {<おろか:.*NOUN>}
	NP-OSORE: {<恐れ:.*NOUN>}
	NP-PPANASHI: {<っぱなし:.*NOUN>}
	NP-ROU: {<ろう者:.*NOUN>}
	NP-SAI: {<際:.*NOUN>}
	NP-SAICHUU: {<最中:.*NOUN>}
	NP-SAIGO: {<最後:.*NOUN>}
	NP-SEI: {<せい:.*NOUN>}
	NP-SHIMATSU: {<始末:.*NOUN>}
	NP-SHITA: {<下:.*NOUN>}
	NP-SHIDAI: {<次第:.*NOUN>}
	NP-SHIKATA: {<しかた:.*NOUN|仕方:.*NOUN>}
	NP-SHOUGA: {<しょうが:.*NOUN>}
	NP-SHUNKAN: {<瞬間:.*NOUN>}
	NP-SOBA: {<そば:.*NOUN>}
	NP-SORE: {<それ:.*NOUN>}
	NP-SOU: {<そう:.*NOUN>}
	NP-SOUI: {<相違:.*NOUN>}
	NP-SUE: {<末:.*NOUN>}
	NP-TABI: {<たび:.*NOUN>}
    NP-TAME: {<たまえ:.*NOUN>}
	NP-TAME: {<ため:.*NOUN>}
	NP-TATE: {<たて:.*NOUN>}
	NP-TARU: {<たる:.*NOUN>}
	NP-TEKI: {<的:.*NOUN>}
	NP-TEMAE: {<手前:.*NOUN>}
	NP-TOCHUU: {<途中:.*NOUN>}
	NP-TEKI: {<て:.*NOUN><き:.*NOUN>}
	NP-TOKORO: {<ところ:.*NOUN>}
	NP-TOKI: {<時:.*NOUN|とき:.*NOUN>}
	NP-TOORI: {<とおり:.*NOUN>}
	NP-TOTAN: {<とたん:.*NOUN>}
	NP-TSUMORI: {<つもり:.*NOUN>}
	NP-TSUIDE: {<ついで:.*NOUN>}
	NP-UCHI: {<うち:.*NOUN>}
	NP-UE: {<上:.*NOUN>}
	NP-YOTEI: {<予定:.*NOUN|よてい:.*NOUN>}
	NP-YOU: {<よう:.*NOUN>}
	NP-YUUMEI: {<有名:.*NOUN>}
	NP-WAKE: {<わけ:.*NOUN>}
	NP-WARI: {<割:.*NOUN|わり:.*NOUN>}
	NP-YOSO: {<よそ:.*NOUN>}
	NP-ZUKUME: {<ずくめ:.*NOUN>}

 	NP: {<.*:NOUN>}


	E-cPASTdattap: {<だっ:.*><.*:TA>}
	E-pPASTn: {<.*:MASU><.*:SEN><.*:DESU><.*:TA>}												# masen deshita
	E-pPRESn: {<.*:MASU><.*:SEN>}																# masen
	E-cPASTn: {<.*:NAI><.*:TA>}																	# nakatta
	E-cTEn: {<.*:NAI><.*:TE>}																	# naide
	E-cPRESn: {<.*:NAI>}																		# nai

 	E-pPASTp: {<.*:MASU><.*:TA>}																# mashita
 	E-pPRESp: {<.*:MASU>}																		# masu
 	E-cPASTp: {<.*:TA>}																			# ta
 	E-cTEp: {<.*:TE>}																			# te


	DAKE_DENAKU: {<NP.*><だけ:.*><.*:DE><E-cPRESn>}
	DAKE_DE: {<NP.*><だけ:.*><.*:DE>}
	DAKE_WA: {<.*:Vdict><だけ:.*><は:.*><.*>*<.*:Vconj|.*:Vstem2|.*:Vstem12><E-.*>}
	V-cDAKE_ATTE: {<NP.*><だけ:.*>(<の:.*><NP-KOTO><は:.*>)?<あっ:.*><E-cTEp>}
	NP-DAKE: {<NP.*><だけ:.*>}

####### Phrase +
	AN_NO_JOU: {<案の定:.*>}
	TOKORO_KARA: {<NP-TOKORO><から:.*>}
	TO_BAKARI_NI: {<と:.*><ばかり:.*><に:.*>}
	SUKUNAKU_TOMO: {<少なくとも:.*>}
	SOU_SURU_TO: {<NP-SOU><する:.*><と:.*>}
	SOU_IEBA: {<NP-SOU><いえ:.*><ば:.*>}
	SORE_NI_SHITEMO: {<それにしても:.*>}
	SORE_NARA: {<それなら:.*>}
	SORE_NA_NONI: {<それなのに:.*>}
	SONO_UE: {<その:.*><NP-UE>}
	SHIKAMO: {<しかも:.*>}

####### NP + 
    BA_SORE_MADE_DA: {<.*:Vba><ば:.*><NP-SORE><まで:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    MADE_DA: {<.*:Vconj|.*:Vstem2|.*:Vstem12>(<の:.*><NP-KOTO>)?<E-cPASTp><まで:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    MADE_DA: {<.*:Vdict>(<の:.*><NP-KOTO>)?<まで:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    MADE_DA: {<それ:.*|これ:.*><まで:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    NP-MADE_: {<NP.*><まで:.*>}

    [X]_GA_[X]_NARA_[Y]_MO_[Y]_DA: {<NP.*><なら:.*><、:.*>?<NP.*><も:.*><NP.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}

    TARI_TOMO: {<NP.*><たり:.*><と:.*><も:.*>}
    TO_IEBA: {<NP.*><と:.*><言え:.*|いえ:.*><ば:.*>}
    TO_IU_TO: {<NP.*><と:.*><言う:.*|いう:.*><と:.*>}
    NDATTE: {<NP.*><な:.*><NP-N><です:.*><って:.*>}
    NDATTE: {<NP.*><な:.*><NP-N><だって:.*>}
    DATTE: {<NP.*><だって:.*>}
    DENAKUTE_NAN_DAROU: {<NP.*><.*:DE><E-cTEn><NP-NAN><E-cPASTp><う:.*>}
    IGAI: {<NP.*><NP-IGAI><の:.*|は:.*|に:.*>?}
    NO_UE_DE_WA: {<NP.*><の:.*><NP-UE><E-cTEp><は:.*>?}
    JOU: {<NP.*><NP-UE><の:.*>}
    JOU: {<NP.*><NP-UE>}
    KARA_SHITE: {<NP.*><から:.*><し.*><E-cTEp>}
    GURUMI: {<NP.*><NP-GURUMI>}
    KATAGATA: {<NP.*><NP-KATAGATA>}
    KOSO: {<NP.*><こそ:.*>}
    MAMIRE: {<NP.*><NP-MAMIRE>}
    NAMI: {<NP.*><NP-NAMI>}
    NARA_DEWA: {<NP.*><NP-NARADEWA>}
    SHIDAI_DE: {<NP.*><NP-SHIDAI><E-cTEp><は:.*>?}
    SHIDAI_DE: {<NP.*><NP-SHIDAI><.*:DE>}
    DE_ARE/DE_AROU_TO: {<NP.*><.*:DE><あろ:.*><う:.*><と:.*>}
    DE_ARE/DE_AROU_TO: {<NP.*><.*:DE><あれ:.*>}
    IKANARU: {<いかなる:.*><NP.*>}
    IKAN_DEWA: {<NP.*><NP-IKAN><E-cTEp><は:.*>?}
    IKAN_DEWA: {<NP.*><NP-IKAN><E-cPASTp>}
    IKAN_DEWA: {<NP.*><NP-IKAN><によって:.*><は:.*>?}
    IWAYURU: {<いわゆる:.*><NP.*>}
    KARA_IU_TO: {<NP.*><から:.*><言う:.*><と:.*>}
    KARA_IU_TO: {<NP.*><から:.*><言え:.*><ば:.*>}
    KARA_IU_TO: {<NP.*><から:.*><言っ:.*><E-cTEp>}
    KARA_MIRU_TO: {<NP.*><から:.*><見る:.*|みる:.*><と:.*>}
    KARA_MIRU_TO: {<NP.*><から:.*><見え:.*|みえ:.*><ば:.*>}
    KARA_MIRU_TO: {<NP.*><から:.*><見:.*|み:.*><E-cTEp>}
    KARA_SURU_TO/KARA_SUREBA: {<NP.*><から:.*><する:.*><と:.*>}
    KARA_SURU_TO/KARA_SUREBA: {<NP.*><から:.*><すれ:.*><ば:.*>}
    KURAI_NO_MONO_DA: {<NP.*><くらい:.*|ぐらい:.*><の:.*|な:.*><NP-MONO><E-cPASTp>}
    NARI_TOMO: {<NP.*><なり:.*><と:.*><も:.*>}
    NARI_TOMO: {<NP.*><なり:.*><とも:.*>}
    NASHI_NI: {<NP.*><なし:.*><に:.*>}
    NASHI_NI: {<NP.*><なし:.*><E-cPASTp><は:.*>}
    NUKI_NI_SHITE/NUKI_DE: {<NP.*><NP-NUKI><に:.*><し:.*><E-cTEp><は:.*>?}
    NUKI_NI_SHITE/NUKI_DE: {<NP.*><NP-NUKI><E-cTEp><は:.*>?}
    NUKI_NI_SHITE/NUKI_DE: {<NP.*><NP-NUKI><に:.*><は:.*>?}
    ZUKUME: {<NP.*><NP-ZUKUME>}
    WA_MOTO_YORI: {<NP.*><は:.*><もとより:.*>}
    WA_SATEOKI: {<NP.*><は:.*><さておき:.*>}
    WA_TOMOKAKU: {<NP.*><は:.*><ともかく:.*><として:.*>?}
    WA_ORO_KA: {<NP.*><は:.*><NP-OROKA>}
    OKI_NI: {<NP.*><NP-OKI><に:.*>}
    TOKITARA: {<NP.*><NP-TOKI|とき:.*><たら:.*>}
    TOTE: {<NP.*><と:.*><E-cTEp>}
    MADASHIMO: {<NP.*><は:.*><まだ:.*><しも:.*>}
    MADASHIMO: {<NP.*><は:.*><まだしも:.*>}
    MADASHIMO: {<NP.*><E-cPASTp><まだ:.*><しも:.*>}
    MADASHIMO: {<NP.*><E-cPASTp><まだしも:.*>}
    SAE: {<NP.*><E-cTEp>?<さえ:.*><も:.*>?}
    SURA/DE_SURA: {<NP.*><で:.*|に:.*>?<すら:.*>}
    V-pKARA_TSUKURU: {<NP.*><から:.*|E-cTEp*><作ら:.*><れ:.*><E-p.*>}
    V-cKARA_TSUKURU: {<NP.*><から:.*|E-cTEp*><作ら:.*><れ:.*><E-c.*>}
    V-cKARA_TSUKURU: {<NP.*><から:.*|E-cTEp*><作ら:.*><れる:.*>}
    V-pKARA_TSUKURU: {<NP.*><から:.*|E-cTEp*><作り:.*><E-p.*>}
    V-cKARA_TSUKURU: {<NP.*><から:.*|E-cTEp*><作ら:.*><E-c.*n>}
    V-cKARA_TSUKURU: {<NP.*><から:.*|E-cTEp*><作っ:.*><E-cPASTp>}
    V-cKARA_TSUKURU: {<NP.*><から:.*|E-cTEp*><作る:.*>}





    ATTE_NO: {<NP.*><あっ.*><E-cTEp><の:.*><NP.*>}
    OYOBI: {<NP.*><および:.*|及び:.*><NP.*>}
    JIMITA: {<NP.*><じみ:.*><E-cPASTp><NP.*>}
    KITTE_NO: {<NP.*><きっ:.*><E-cTEp><の:.*><NP.*>}
    NOMIKA: {<NP.*><のみ:.*><か:.*><、:.*>?<NP.*>}
    TARU: {<NP.*><NP-TARU><NP.*>}
    TO_IWAZU: {<NP.*><と:.*><いわ:.*><ず:.*><、:.*>?<NP.*><と:.*><いわ:.*><ず:.*>}
    TO_II~TO_II: {<NP.*><と:.*><いい:.*><、:.*>?<NP.*><と:.*><いい:.*>}

    O_TSUUJITE/O_TOOSHITE: {<NP.*><を通して:.*|を通じて:.*>}
 	O_KOMETE: {<NP.*><を:.*><込め:.*|こめ.*><E-cTEp>}
 	O_FUMAETE: {<NP.*><を:.*><踏まえ:.*><E-cTEp>?}
    O_HAJIME: {<NP.*><を:.*><NP-HAJIME><と:.*><し:.*><E-p.*>}
 	O_HAJIME: {<NP.*><を:.*><NP-HAJIME><と:.*><し:.*><E-c.*>}
 	O_HAJIME: {<NP.*><を:.*><NP-HAJIME><と:.*><する:.*>}
    O_HAJIME: {<NP.*><を:.*><NP-HAJIME>}
    O_HETE: {<NP.*><を:.*><経:.*><E-cTEp>}
    O_KAERIMIZU: {<NP.*><を:.*|も:.*><かえりみ:.*><ず:.*>} 
    O_KANETE: {<NP.*><を:.*|も:.*><兼ね:.*><E-cTEp>}
    O_KEIKI_NI: {<NP.*><を:.*><NP-KEIKI><に:.*|として:.*>}
    O_KI_NI: {<NP.*><を:.*><NP-KI><に:.*>}
    O_KINJIENAI: {<NP.*><を:.*><禁じ:.*><え:.*><E-.*n>}
    O_KAGIRI_NI: {<NP.*><を:.*><NP-KAGIRI><に:.*|E-cTEp>}
    O_NOZOITE: {<NP.*><を:.*><除い:.*><E-cTEp><は:.*>?}
    O_NOZOITE: {<NP.*><を:.*><除け:.*><ば:.*>}
    O_MONOTOMO_SEZU: {<NP.*><を:.*><NP-MONO><と:.*><も:.*><せ:.*><ず:.*>}
    O_MOTTE: {<NP.*><を:.*><もっ:.*><E-cTEp>}
    O_MOTO_NI: {<NP.*><を:.*><NP-MOTO><に:.*>(<し.*><E-cTEp>)?}
    O_TOWAZU: {<NP.*><を:.*><問わ:.*><ず:.*>}
    O_YOSO_NI: {<NP.*><を:.*><NP-YOSO><に:.*>}

    O_CHUUSHIN_NI: {<NP.*><を:.*><NP-CHUUSHIN><と:.*><し:.*><E-p.*>}
    O_CHUUSHIN_NI: {<NP.*><を:.*><NP-CHUUSHIN><と:.*><し:.*><E-c.*>}
    O_CHUUSHIN_NI: {<NP.*><を:.*><NP-CHUUSHIN><と:.*><する:.*>}
    O_CHUUSHIN_NI: {<NP.*><を:.*><NP-CHUUSHIN><に:.*>}
    O_KAWAKIRI_NI: {<NP.*><を:.*><NP-KAWAKIRI><と:.*><し:.*><E-p.*>}
    O_KAWAKIRI_NI: {<NP.*><を:.*><NP-KAWAKIRI><と:.*><し:.*><E-c.*>}
    O_KAWAKIRI_NI: {<NP.*><を:.*><NP-KAWAKIRI><と:.*><する:.*>}
    O_KAWAKIRI_NI: {<NP.*><を:.*><NP-KAWAKIRI><に:.*>}

    NI_SHITAGATTE: {<.*:Vdict><に従って:.*>}								# order adj ku/ni naru ni shigatte
    NI_SHITAGATTE: {<NP.*><に従って:.*>}
    NI_SHITAGATTE: {<.*:Vdict><に従い:.*|にしたが>}								# order adj ku/ni naru ni shigatte
    NI_SHITAGATTE: {<NP.*><に従い:.|にしたが*>}
    NI_SHITAGATTE: {<.*:Vdict><に:.*><したがっ:.*><E-cTEp>}								# order adj ku/ni naru ni shigatte
    NI_SHITAGATTE: {<NP.*><に:.*><したがっ:.*><E-cTEp>}
    NI_SHITAGATTE: {<.*:Vdict><に:.*><したがい:.*>}								# order adj ku/ni naru ni shigatte
    NI_SHITAGATTE: {<NP.*><に:.*><したがい:.*>}

    NI_WATATTE: {<NP.*><にわたって:.*>}
    NI_ATTE: {<NP.*><に:.*><あっ:.*><E-cTEp><は:.*>?}
    NI_HANSURU: {<NP.*><に:.*><反し:.*><E-.*>}
    NI_HANSURU: {<NP.*><に:.*><反する:.*>}
    NI_HANSURU: {<NP.*><に反する.*>}
    NI_ITARU_MADE: {<NP.*><に:.*><至る:.*|いたる:.*><まで:.*>}
    NI_ITATTE_WA: {<NP.*><に:.*><至っ:.*|いたっ:.*><E-cTEp><は:.*>}
    NI_IWASEREBA: {<NP.*><に:.*><言わ:.*><せれ:.*><ば:.*>}
	NI_KAGITTA_KOTO_DE_WA_NAI: {<NP.*><に:.*><限っ:.*><E-cPASTp><NP-KOTO><.*:DE><は:.*><E-cPRESn>}
    NI_KAGITTE: {<NP.*><に:.*><限っ:.*><E-cTEp*>}
    NI_KAGIRAZU: {<NP.*><に:.*><限ら:.*><ず:.*>}
    KARA~NI_KAKETE: {<NP.*><から:.*><NP.*><にかけて:.*>}
    NI_KAKETE: {<NP.*><にかけて:.*><は:.*|も:.*>?}
    NI_KAN_SURU/NI_KAN_SHITE: {<NP.*><に関する:.*>}
    NI_KAN_SURU/NI_KAN_SHITE: {<NP.*><に関して:.*>}
    NI_KAWATTE/NI_KAWARI: {<NP.*><に:.*><かわり:.*>}
    NI_KAWATTE/NI_KAWARI: {<NP.*><に:.*><かわっ:.*><E-cTEp>}
    NI_KOTAETE: {<NP.*><に:.*><応え:.*|こたえ:.*><E-cTEp>?}
    NI_KOTAETE: {<NP.*><に:.*><応える:.*|こたえる:.*>}
    NI_KURABETE: {<NP.*><に:.*><比べ:.*><E-cTEp>?}
    NI_KURABETE: {<NP.*><に:.*><比べる:.*><と:.*>}
    NI_KURABETE: {<NP.*><に:.*><比べれ:.*><ば:.*>}
    NI_KUWAETE: {<NP.*><に:.*><加え:.*><E-cTEp*>}
    NI_MOMASHITE: {<NP.*><に:.*><も:.*><まして:.*>}
    NI_MATSUWARU: {<NP.*><にまつわる:.*>}
    NI_MOTOZUITE: {<NP.*><に:.*><基づい:.*><E-cTEp>}
    NI_MOTOZUITE: {<NP.*><に:.*><基づき:.*>}
    NI_MUKATTE: {<NP.*><に:.*><向かっ:.*><E-cTEp>}
    NI_MUKATTE: {<NP.*><に:.*><向け:.*><E-cTEp>}
    NI_NARERU: {<NP.*><に:.*><なれ:.*|慣れ:.*><E-.*>}
    NI_NARERU: {<NP.*><に:.*><なれる:.*|慣れる:.*>}
    NI_NOTTOTTE: {<NP.*><に:.*><則っ:.*><E-cTEp>}
    NI_OUJITE: {<NP.*><に:.*><応じ:.*><E-cTEp|E-cPASTp>}
    NI_OITE/NI_OKERU: {<NP.*><において.*>}
    NI_OITE/NI_OKERU: {<NP.*><における.*><NP.*>}
    NI_SAKI_GAKETE: {<NP.*><に:.*><先駆け:.*><E-cTEp>}
    NI_SHITARA/NI_SUREBA: {<NP.*><に:.*><し:.*><たら:.*>}
    NI_SHITARA/NI_SUREBA: {<NP.*><に:.*><すれ:.*><ば:.*>}
    NI_SOKUSHITE: {<NP.*><に:.*><即し:.*><E-cTEp|E-cPASTp>?}
    NI_SOTTE: {<NP.*><に:.*><沿っ:.*><E-cTEp|E-cPASTp>}
    NI_SOTTE: {<NP.*><に:.*><沿い:.*|沿う:.*>}
    NI_TAISHITE: {<NP.*><に対して.*>}
    NI_TOTTE: {<NP.*><にとって.*><は:.*|も:.*>?}
    NI_TSUITE: {<NP.*><について.*>}
    NI_TSUKI:{<NP.*><に:.*><つき:.*>}
    NITE:{<NP.*><にて:.*>}
    NI_TERASHITE: {<NP.*><に:.*><照らし:.*><E-cTEp|E-cPASTp>?}
    NI_YORAZU: {<NP.*><に:.*><よら:.*><ず:.*>}
    NI_YORU_TO/NI_YOREBA: {<NP.*><に:.*><よる:.*><と.*>}
    NI_YORU_TO/NI_YOREBA: {<NP.*><に:.*><よれ:.*><ば:.*>}
    NI_YOTTE/NI_YORU: {<NP.*><によって:.*|により:.*|による:.*>}
    NI_TODOMARAZU: {<NP.*><に:.*><とどまら:.*><ず:.*>}


    NO_ITARI: {<NP.*><の:.*><NP-ITARI>}
    NO_KIWAMI: {<NP.*><の:.*><NP-KIWAMI>}
    NO_MOTO_DE: {<NP.*><の:.*><NP-SHITA><に:.*|と:.*|E-cTEp>}

    TOMONAKU: {<.*:Vdict><とも:.*><なく:.*|なし:.*>}
    TOMONAKU: {<.*:Vdict><と:.*><も:.*><なく:.*|なし:.*>}


    TO_ITTA: {<NP.*><といった:.*>}
    TSU~TSU: {<.*:Vstem1|.*:Vstem12><つ:.*><Vindef:.*>?<.*:Vstem1|.*:Vstem12><つ:.*>}


 	TEKI: {<NP.*><NP-TEKI>}
 	NP-cBA: {<NP.*><なら:.*><ば:.*>}
  	NP-cBA: {<NP.*><.*:DE><E-cPRESn><ば:.*>}


##### SENTENCE 2nd

    BIRU: {<NP.*|.*:ADJ-I><びて:.*|びる:.*>}
    BIRU: {<NP.*|.*:ADJ-I><びた:.*><NP.*>}
    BIRU: {<悪びれる:.*>}
    BIRU: {<古び:.*><E-cPASTp>}


    SOU_DA2: {<.*:Vstem1|.*:Vstem12|.*:ADJ.*><そう:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}			#rest of the rule is down

  	V-pSUGIRU: {<.*:Vstem1|.*:Vstem12><すぎ:.*><E-p.*>}
  	V-pSUGIRU: {<.*:ADJ-I.*><すぎ:.*><E-p.*>}
  	V-pSUGIRU: {<.*:ADJ-NA><すぎ:.*><E-p.*>}
  	V-cSUGIRU: {<.*:Vstem1|.*:Vstem12><すぎ:.*><E-c.*>}
  	V-cSUGIRU: {<.*:ADJ-I.*><すぎ:.*><E-c.*>}
  	V-cSUGIRU: {<.*:ADJ-NA><すぎ:.*><E-c.*>}
  	V-cSUGIRU: {<.*:Vstem1|.*:Vstem12><すぎる:.*>}
  	V-cSUGIRU: {<.*:ADJ-I.*><すぎる:.*>}
  	V-cSUGIRU: {<.*:ADJ-NA><すぎる:.*>}

    NIKUI: {<.*:Vstem1|.*:Vstem12><にくい:.*>}
    YASUI: {<.*:Vstem1|.*:Vstem12><やすい:.*>}
    GATAI: {<.*:Vstem1|.*:Vstem12><がたい:.*>}
	ZURAI: {<.*:Vstem1|.*:Vstem12><づらい:.*>}

	RASHII: {<.*:V.*|NP.*|ADJ-NA|ADJ-Idict><らしい:.*|らしく:.*>}

	BURI: {<.*:Vstem1|.*:Vstem12><っ:.*>?<NP-BURI>}
	BURI: {<NP.*><NP-BURI>}



##### SENTENCE middle	
	DAKE_MASHI_DA: {<.*:V.*><E-c.*>?<だけ:.*><E-pPASTp >}
	DAKE_MASHI_DA: {<.*:ADJ-Idict><だけ:.*><E-pPASTp >}
	DAKE_MASHI_DA: {<.*:ADJ-NA><な:.*><だけ:.*><E-pPASTp >}
	DAKE_MASHI_DA: {<NP.*>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<だけ:.*><E-pPASTp >}

	DEWA_SUMANAI: {<.*:V.*><E-c.*>?<E-cTEp><は:.*><すま:.*><E-cPRESn>}
	DEWA_SUMANAI: {<NP.*><E-cTEp><は:.*><すま:.*><E-cPRESn>}

	NIMO_KAKAWARAZU: {<.*:V.*><E-c.*>?<に:.*><も:.*><関わら:.*|かかわら:.*><ず:.*>}
	NIMO_KAKAWARAZU: {<.*:ADJ-Idict><に:.*><も:.*><関わら:.*|かかわら:.*><ず:.*>}
	NIMO_KAKAWARAZU: {<NP.*|.*:ADJ-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)?<に:.*><も:.*><関わら:.*|かかわら:.*><ず:.*>}


	NI_KAKAWARAZU: {<.*:Vindef><E-cPRESn><に:.*><かかわら:.*><ず:.*>}
	NI_KAKAWARAZU: {<.*:Vdict|NP.*|ADJ-.*><に:.*><かかわら:.*><ず:.*>}

	NI_SUGINAI: {<.*:V.*><E-c.*>?<に:.*><過ぎ:.*|すぎ:.*><E-.*n>}
	NI_SUGINAI: {<.*:ADJ-Idict.*><に:.*><過ぎ:.*|すぎ:.*><E-.*n>}
	NI_SUGINAI: {<NP.*|.*:ADJ-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)?<に:.*><過ぎ:.*|すぎ:.*><E-.*n>}


	NI_TOMONATTE: {<.*:Vdict|NP.*><に:.*><伴っ:.*><E-cTEp>}
	NI_TOMONATTE: {<.*:Vdict|NP.*><に:.*><伴い:.*|伴う:.*>}

    NO_GA_HETA: {<.*:Vdict><NP-NO><が:.*><下手:.*|へた:.*>}
    NO_GA_JOUZU: {<.*:Vdict><NP-NO><が:.*><上手:.*|じょうず:.*>}
    NO_GA_SUKI: {<.*:Vdict><NP-NO><が:.*><好き:.*|すき:.*>}

    MO_KAMAWAZU: {<.*:V.*><E-c.*><NP-NO><も:.*><構わ:.*|かまわ:.*><ず:.*>}
    MO_KAMAWAZU: {<.*:Vdict><NP-NO><も:.*><構わ:.*|かまわ:.*><ず:.*>}
    MO_KAMAWAZU: {<NP.*><も:.*><構わ:.*|かまわ:.*><ず:.*>}

  	MATAWA: {<NP.*><又は:.*|または:.*><NP.*>}

  	HOU_GA_MASHI_DA: {<NP-HOU><が:.*><まし:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}

    KARA_TO_ITTE: {<.*:V.*><E-c.*><から:.*><と:.*><言っ:.*|いっ:.*><E-cTEp>}
    KARA_TO_ITTE: {<NP.*|.*:ADJ-NA><です:.*|E-cPASTp|E-cPASTdattap|でした:.*><から:.*><と:.*><言っ:.*|いっ:.*><E-cTEp>}
    KARA_TO_ITTE: {<.*:ADJ-Idict><から:.*><と:.*><言っ:.*|いっ:.*><E-cTEp>}

	KA_TO_OMOTTARA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><か:.*><と:.*><思っ:.*><たら:.*>}
	KA_TO_OMOTTARA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><か:.*><と:.*><思う:.*><と:.*>}
	KA_TO_OMOTTARA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><か:.*><と:.*><思え:.*><ば:.*>}

	KOSO_SURE: {<NP.*|.*:Vstem1|.*:Vstem12><こそ:.*><すれ:.*>}

	NI_SAKIDACHI: {<.*:Vdict|NP.*><に:.*><先立ち:.*>}
	NI_SAKIDACHI: {<.*:Vdict|NP.*><に:.*><先立っ:.*><E-cTEp>}
	NI_SAKIDACHI: {<.*:Vdict|NP.*><に:.*><先立つ:.*>}

	GATERA: {<.*:Vstem1|.*:Vstem12><が:.*><てら:.*>}
	GATERA: {<NP.*><が:.*><てら:.*>}

 	TARA: {<.*:ADJ-NA><E-cPASTp><.*:TARA>}
 	TARA: {<.*:ADJ-NA><じゃ:.*><E-cPRESn><.*:TARA>}
 	TARA: {<.*:ADJ-I.*><.*:TARA>}
  	TARA: {<.*:ADJ-I.*><E-cPRESn><.*:TARA>}

 	TE_TOUZEN_DA: {<.*:Vstem.*|.*:ADJ-.*><E-cTEp><当然:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	TE_TOUZEN_DA: {<.*:Vstem.*|.*:ADJ-.*><E-cTEp><当たり前:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}


  	TO_ATTE: {<.*:V.*><E-c.*>?<と:.*><あっ:.*><E-cTEp>}
  	TO_ATTE: {<NP.*|.*:ADJ-.*><と:.*><あっ:.*><E-cTEp>}

    TO_IU_KA~TO_IU_KA: {<NP.*|.*:ADJ.*><という:.*><か:.*><、:.*>?<NP.*|.*:ADJ.*><という:.*><か:.*>}
    TO_IU_KA~TO_IU_KA: {<NP.*|.*:ADJ.*><と:.*><いう:.*><か:.*><、:.*>?<NP.*|.*:ADJ.*><と:.*><いう:.*><か:.*>}

  	TO_OMOIKIYA: {<と:.*><思い:.*><き:.*><や:.*>}


##### SENTENCE end
	KAMO_SHIRENAI: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><かも:.*>(<しれ:.*><E-.*PRESn>)?}
	KAMO_SHIRENAI: {<.*:Vindef><E-c.*n><かも:.*>(<しれ:.*><E-.*PRESn>)?}
	KAMO_SHIRENAI: {<.*:Vdict><かも:.*>(<しれ:.*><E-.*PRESn>)?}
	KAMO_SHIRENAI: {<NP.*><かも:.*>(<しれ:.*><E-.*PRESn>)?}

    TE_ITADAKEMASEN_KA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><.*:TE><い:.*><E-cPASTp><だけ:.*><E-pPRESn><か:.*>}

    O~KUDASAI: {<お:.*|ご:.*><.*:Vstem1|.*:Vstem12><ください:.*|下さい:.*>}
	O~KUDASAI: {<NP-O/GO_><ください:.*|下さい:.*>}
 	O_KUDASAI: {<NP.*><を:.*><NP.*>?<ください:.*|下さい:.*>}
    NAIDE_KUDASAI: {<.*:Vindef><E-cTEn><ください:.*>}

    MASHOU_KA: {<.*:Vstem1|.*:Vstem12><E-pPRESp><う:.*><か:.*>}
    MASHOU: {<.*:Vstem1|.*:Vstem12><E-pPRESp><う:.*>}

	NAKUSHITE: {<なく:.*><し:.*><E-cTEp>}

    TOWA_IU_MONO_NO: {<と:.*><は:.*><いう:.*><NP-MONO><の:.*>}
    TOWA_IU_MONO_NO: {<と:.*><は:.*><いう:.*><ものの:.*>}


    TO_IU_YORI: {<.*:V.*|V-c.*><E-c.*>?<と:.*><いう:.*><より:.*>}
    TO_IU_YORI: {<NP.*|.*:ADJ-Idict|.*:ADJ-NA><E-c.*>?<と:.*><いう:.*><より:.*>}

	TO_IU:{<と:.*><言う:.*|いう:.*>}
	TO_IU:{<という:.*>}
	TO_IU:{<と:.*><いい:Vstem1><E-.*>}
    TO_ITTEMO_II: {<と:.*><いっ:.*|言っ:.*><E-cTEp><も:.*><いい:.*>}
    TO_ITTEMO: {<.*:V.*|V-c.*><E-c.*>?<、:.*>?<と:.*><いっ:.*|言っ:.*><E-cTEp><も:.*>}
    TO_ITTEMO: {<.*:ADJ-Idict><、:.*>?<と:.*><いっ:.*|言っ:.*><E-cTEp><も:.*>}
    TO_ITTEMO: {<NP.*|.*:ADJ-NA><E-cPASTp>?<、:.*>?<と:.*><いっ:.*|言っ:.*><E-cTEp><も:.*>}

    TE_HAJIMETE: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><はじめ:.*><E-cTEp>}
    TE_HAJIMETE: {<.*:Vstem1|.*:Vstem12><たく:助動詞><E-cTEp><はじめ:.*><E-cTEp>}
    TE_ITE_WA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><い:.*><E-cTEp>}
    TE_ITE_WA: {<.*:Vstem1|.*:Vstem12><たく:助動詞><E-cTEp><い:.*><E-cTEp>}
    TE_TAMARANAI: {<.*:ADJ-NA><.*:DE><たまらない:.*>}
    TE_TAMARANAI: {<.*:ADJ-I><E-cTEp><たまらない:.*>}
    TE_TAMARANAI: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><たまらない:.*>}
    TE_TAMARANAI: {<.*:Vstem1|.*:Vstem12><たく:助動詞><E-cTEp><たまらない:.*>}

	V-cSOU_MO_NAI/SOU_NI_NAI: {<.*:Vstem1|.*:Vstem12><NP-SOU><に:.*|も:.*><E-.*n|A-NORMnai>}
    BETSU_NI~NAI: {<別に:.*><.*>*<E-.*n|ない:.*>}
    DOU_NIMO~NAI: {<どうにも:.*><.*>*<E-.*n|ない:.*>}
    HODO~NAI: {<NP.*><ほど:.*><.*>*<E-.*n|ない:.*>}
    HOKA_NI~NAI: {<NP-HOKA><に:.*><.*>*<E-.*n|ない:.*>}
    KESSHITE~NAI: {<決して:.*><.*>*<E-.*n|ない:.*>}
    MATTAKU~NAI: {<まったく:.*|全く:.*><.*>*<E-.*n|ない:.*>}
    METTA_NI~NAI: {<滅多に:.*|めったに:.*><.*>*<E-.*n|ない:.*>}
    METTA_NI~NAI: {<NP.*><は:.*><滅多に:.*|めったに:.*><ない:.*>}
    NANI_MO~NAI: {<NP-NANI><も:.*><.*>*<E-.*n|ない:.*>}
    ROKU_NI~NAI: {<ろくに:.*><.*>*<.*>*<E-.*n|ない:.*|無い:.*>}
    ZENZEN~NAI: {<ぜんぜん:.*|全然:.*><.*>*<E-.*n|ない:.*>}
    SUKOSHI_MO~NAI: {<少し:.*><も:.*><.*>*<E-.*n|ない:.*>}
    WA~DE_YUUMEI: {<は:.*><.*>*<E-cTEp><NP-YUUMEI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}


	MO_SHINAIDE: {<.*:Vstem1|.*:Vstem12><も:.*><し:.*><E-cTEn>}
	TATE: {<.*:Vstem1|.*:Vstem12><NP-TATE>}
	TAMAE: {<.*:Vstem1|.*:Vstem12><NP-TAMAE|たまえ:.*>}
	TAMAE: {<.*:Vstem1|.*:Vstem12><E-cPASTp><ま:.*><え:.*>}

	YOU_NI_YOTTE_WA: {<.*:Vstem1|.*:Vstem12><NP-YOU><によって:.*><は:.*>}
	SHIDAI: {<.*:Vstem1|.*:Vstem12><NP-SHIDAI>}

    V-pAGERU: {<.*:Vstem1|.*:Vstem12><あげ:.*|上げ:.*><E-p.*>}
    V-cAGERU: {<.*:Vstem1|.*:Vstem12><あげ:.*|上げ:.*><E-c.*>}
    V-pAGERU: {<.*:Vstem1|.*:Vstem12><あがり:.*|上がり:.*><E-p.*>}
    V-cAGERU: {<.*:Vstem1|.*:Vstem12><あがら:.*|上がら:.*><E-c.*n>}
    V-cAGERU: {<.*:Vstem1|.*:Vstem12><あがっ:.*|上がっ:.*><E-cPASTp>}
    V-cAGERU: {<.*:Vstem1|.*:Vstem12><あげる:.*|あがる:.*|上げる:.*|上がる:.*>}


########### V WORDS
 	V-pPASTpOMOU: {<思い:.*><E-pPASTp>}
 	V-pPASTnOMOU: {<思い:.*><E-pPASTn>}
 	V-pPRESpOMOU: {<思い:.*><E-pPRESp>}
 	V-pPRESnOMOU: {<思い:.*><E-pPRESn>}
 	V-cPASTpOMOU: {<思っ:.*><E-cPASTp>}
  	V-cPRESnOMOU: {<思わ:.*><E-cPRESn>}
 	V-cPRESpOMOU: {<思う:.*>}

  	V-pPASTpARUx: {<あり:.*><E-pPASTp>}
  	V-pPASTnARUx: {<あり:.*><E-pPASTn>}
  	V-pPRESnARUx: {<あり:.*><E-pPRESn>}
  	V-pPRESpARUx: {<あり:.*><E-pPRESp>}
  	V-cPRESnARUx: {<ない:NAI>}
  	V-cPASTnARUx: {<なかっ:.*><E-cPASTp>}
  	V-cPASTpARUx: {<あっ:.*><E-cPASTp>}
  	V-cPRESpARUx: {<ある:.*>}
  	V-TEpARUx: {<あっ:.*><E-cTEp >}

   	V-pPASTpIRUx: {<い:.*><E-pPASTp>}
  	V-pPASTnIRUx: {<い:.*><E-pPASTn>}
  	V-pPRESnIRUx: {<い:.*><E-pPRESn>}
  	V-pPRESpIRUx: {<い:.*><E-pPRESp>}
  	V-cPRESnIRUx: {<い:.*><E-cPRESn>}
  	V-cPASTnIRUx: {<い:.*><E-cPASTp>}
  	V-cPASTpIRUx: {<い:.*><E-cPASTp>}
  	V-cPRESpIRUx: {<いる:.*>}

  	V-pPASTpDEKIRU: {<でき:.*><E-p.*>}
  	V-pPASTnDEKIRU: {<でき:.*><E-p.*>}
  	V-cPRESnDEKIRU: {<でき:.*><E-cPRESn>}
  	V-cPASTnDEKIRU: {<でき:.*><E-cPASTn>}
  	V-cPASTpDELIRU: {<でき:.*><E-c.*p>}
  	V-cPRESpDEKIRU: {<できる:.*>}

 	V-ppNARU: {<なり:.*><E-p.*p>}
 	V-pnNARU: {<なり:.*><E-p.*n>}
 	V-cPASTpNARU: {<なっ:.*><E-cPASTp>}
 	V-cPRESnNARU: {<なら:.*><E-cPRESn>}
 	V-cPRESpNARU: {<なる:.*>}

 	V-pSUMU: {<すみ:.*|済み:.*><E-p.*>}
 	V-cSUMU: {<すん:.*|済ん:.*><E-cPASTp>}
 	V-cSUMU: {<すま:.*|済ま:.*><E-cPRESn>}
 	V-cSUMU: {<すむ:.*|済む:.*>}


########### V RULES AND TE

 	YOU_TO_OMOU: {<.*:Vjo><う:.*><と:.*><思っ:.*><E-cTEp>}	

 	TO_KITE_IRU: {<.*:V.*><E-c.*>?<に:.*><と:.*><き:.*><E-cTEp><V-.*IRUx>}
 	TO_KITE_IRU: {<NP.*|A-NA|A-Idict|A-NORM.*><と:.*><き:.*><E-cTEp><V-.*IRUx>}
   	NI_KIMATTE_IRU: {<.*:V.*><E-c.*>?<に:.*><決まっ:.*><E-cTEp><V-.*IRUx>}
  	NI_KIMATTE_IRU: {<NP.*|A-NA|A-Idict|A-NORM.*><に:.*><決まっ:.*><E-cTEp><V-.*IRUx>}


	V-pENAI: {<.*:Vstem1|.*:Vstem12><得:.*><E-p.*n>}
	V-cENAI: {<.*:Vstem1|.*:Vstem12><得:.*><E-c.*n>}

	V-pKANENAI: {<.*:Vstem1|.*:Vstem12><かね:.*><E-p.*n>}
	V-cKANENAI: {<.*:Vstem1|.*:Vstem12><かね:.*><E-c.*n>}

	V-pKIRENAI: {<.*:Vstem1|.*:Vstem12><切れ:.*><E-p.*n>}
	V-cKIRENAI: {<.*:Vstem1|.*:Vstem12><切れ:.*><E-c.*n>}

	V-pYASHINAI: {<.*:Vstem1|.*:Vstem12><やし:.*><E-cPRESn>}

	V-pAU: {<.*:Vstem1|.*:Vstem12><合い:.*|あい:.*><E-p.*>}
	V-pAU: {<.*:Vstem1|.*:Vstem12><合っ:.*|あっ:.*><E-c.*p>}
	V-pAU: {<.*:Vstem1|.*:Vstem12><合わ:.*|あわ:.*><E-c.*n>}
	V-cAU: {<.*:Vstem1|.*:Vstem12><合う:.*|あう:.*>}

	V-pDASU: {<.*:Vstem1|.*:Vstem12><出し:.*|だし:.*><E-p.*>}
	V-pDASU: {<.*:Vstem1|.*:Vstem12><出し:.*|だし:.*><E-c.*p>}
	V-pDASU: {<.*:Vstem1|.*:Vstem12><出さ:.*|ださ:.*><E-c.*n>}
	V-cDASU: {<.*:Vstem1|.*:Vstem12><出す:.*|だす:.*>}

 	V-pHAJIMERU: {<.*:Vstem1|.*:Vstem12><はじめ:.*|始め:.*><E-p.*>}
 	V-cHAJIMERU: {<.*:Vstem1|.*:Vstem12><はじめ:.*|始め:.*><E-c.*>}
 	V-cHAJIMERU: {<.*:Vstem1|.*:Vstem12><はじめる:.*|始める:.*>}

	V-pKAKERU: {<.*:Vstem1|.*:Vstem12><かけ:.*><E-p.*>}
	V-pKAKERU: {<.*:Vstem1|.*:Vstem12><かけ:.*><E-c.*p>}
	V-cKAKERU: {<.*:Vstem1|.*:Vstem12><かける:.*|かけの:.*>}
	V-cKAKERU: {<.*:Vstem1|.*:Vstem12><かけ:.*><の:.*>}

	V-pKANERU: {<.*:Vstem1|.*:Vstem12><かね:.*><E-p.*>}
	V-pKANERU: {<.*:Vstem1|.*:Vstem12><かね:.*><E-c.*p>}
	V-cKANERU: {<.*:Vstem1|.*:Vstem12><かねる:.*>}

	V-pKIRU: {<.*:Vstem1|.*:Vstem12><切:.*|切れ:.*><E-p.*>}
	V-pKIRU: {<.*:Vstem1|.*:Vstem12><切:.*|切れ:.*><E-c.*p>}
	V-cKIRU: {<.*:Vstem1|.*:Vstem12><切る:.*|切れる:.*>}

	V-pKOMU: {<.*:Vstem1|.*:Vstem12><込み:.*|こみ:.*><E-p.*>}
	V-pKOMU: {<.*:Vstem1|.*:Vstem12><込ん:.*|こん:.*><E-c.*p>}
	V-pKOMU: {<.*:Vstem1|.*:Vstem12><込ま:.*|こま:.*><E-c.*n>}
	V-cKOMU: {<.*:Vstem1|.*:Vstem12><込む:.*|こむ:.*>}

	V-pNAOSU: {<.*:Vstem1|.*:Vstem12><直し:.*|なおし:.*><E-p.*>}
	V-pNAOSU: {<.*:Vstem1|.*:Vstem12><直し:.*|なおし:.*><E-c.*p>}
	V-pNAOSU: {<.*:Vstem1|.*:Vstem12><直さ:.*|なおさ:.*><E-c.*n>}
	V-cNAOSU: {<.*:Vstem1|.*:Vstem12><直す:.*|なおす:.*>}

	V-pNUKU: {<.*:Vstem1|.*:Vstem12><抜き:.*><E-p.*>}
	V-pNUKU: {<.*:Vstem1|.*:Vstem12><抜い:.*><E-cPASTp>}
	V-pNUKU: {<.*:Vstem1|.*:Vstem12><抜か:.*><E-c.*n>}
	V-cNUKU: {<.*:Vstem1|.*:Vstem12><抜く:.*>}

	V-pOWARU: {<.*:Vstem1|.*:Vstem12><終わり:.*><E-p.*>}
	V-pOWARU: {<.*:Vstem1|.*:Vstem12><終わ:.*><E-c.*p>}
	V-pOWARU: {<.*:Vstem1|.*:Vstem12><終わら:.*><E-c.*n>}
	V-cOWARU: {<.*:Vstem1|.*:Vstem12><終わる:.*>}

	V-pTOOSU: {<.*:Vstem1|.*:Vstem12><通し:.*|とおし:.*><E-p.*>}
	V-pTOOSU: {<.*:Vstem1|.*:Vstem12><通し:.*|とおし:.*><E-c.*p>}
	V-pTOOSU: {<.*:Vstem1|.*:Vstem12><遠さ:.*|とおさ:.*><E-c.*n>}
	V-cTOOSU: {<.*:Vstem1|.*:Vstem12><通す:.*|とおす:.*>}

	V-pTSUZUKERU: {<.*:Vstem1|.*:Vstem12><続け:.*><E-p.*>}
	V-pTSUZUKERU: {<.*:Vstem1|.*:Vstem12><続け:.*><E-c.*p>}
	V-cTSUZUKERU: {<.*:Vstem1|.*:Vstem12><続ける:.*>}

	V-pERU/URU: {<.*:Vstem1|.*:Vstem12><得:.*|え:.*|う:.*><E-p.*>}
	V-pERU/URU: {<.*:Vstem1|.*:Vstem12><得:.*|え:.*|う:.*><E-c.*p>}
	V-cERU/URU: {<.*:Vstem1|.*:Vstem12><得る:.*|える:.*|うる:.*>}

#NARU
 	V-pYOU_NI_NARU: {<.*:Vindef><E-cPRESn><NP-YOU><に:.*><V-p.*NARU>}
 	V-cYOU_NI_NARU: {<.*:Vindef><E-cPRESn><NP-YOU><に:.*><V-c.*NARU>}
 	V-pYOU_NI_NARU: {<.*:Vdict><NP-YOU><に:.*><V-p.*NARU>}
 	V-cYOU_NI_NARU: {<.*:Vdict><NP-YOU><に:.*><V-c.*NARU>}

  	V-pHAME_NI_NARU: {<.*:Vdict><NP-HAME><に:.*><V-p.*NARU>}
  	V-cHAME_NI_NARU: {<.*:Vdict><NP-HAME><に:.*><V-c.*NARU>}


 	V-pKOTO_NI_NARU: {<NP-KOTO1.*><に:.*><V-p.*NARU>}
 	V-cKOTO_NI_NARU: {<NP-KOTO1.*><に:.*><V-c.*NARU>}

    V-pO~NI_NARU: {<お:.*|ご:.*><.*:Vstem1|.*:Vstem12><に:.*><V-p.*NARU>}
    V-cO~NI_NARU: {<お:.*|ご:.*><.*:Vstem1|.*:Vstem12><に:.*><V-c.*NARU>}
	V-pO~NI_NARU: {<NP-O/GO_><に:.*><V-c.*NARU>}
	V-cO~NI_NARU: {<NP-O/GO_><に:.*><V-c.*NARU>}

 	V-pNI_NARU/KU_NARU: {<NP.*|.*:ADJ-NA><に:.*><V-p.*NARU>}
 	V-cNI_NARU/KU_NARU: {<NP.*|.*:ADJ-NA><V-c.*NARU>}
 	V-pNI_NARU/KU_NARU: {<.*:ADJ-I><V-p.*NARU>}
 	V-cNI_NARU/KU_NARU: {<.*:ADJ-I><V-c.*NARU>}

#IKU
 	V-pNI_IKU: {<.*:Vstem1|.*:Vstem12><に:.*><いき:.*|行き:.*><E-p.*>}
  	V-cNI_IKU: {<.*:Vstem1|.*:Vstem12><に:.*><いっ:.*|行っ:.*><E-cPASTp>}
  	V-cNI_IKU: {<.*:Vstem1|.*:Vstem12><に:.*><いっ:.*|行か:.*><E-cPASTn>}
 	V-cNI_IKU: {<.*:Vstem1|.*:Vstem12><に:.*><いく:.*|行く:.*>}



#SURU
 	V-SHITATTE: {<し:Vstem12><E-cPASTp><って:.*>}
    NI_SHITE: {<NP.*><に:.*><し.*><E-cTEp>}


	TARI~TARI: {<.*:Vconj|.*:Vstem2|.*:Vstem12><たり:.*><.*>*<.*:Vconj|.*:Vstem2|.*:Vstem12><たり:.*><し:.*><E-.*>}
	TARI~TARI: {<.*:Vconj|.*:Vstem2|.*:Vstem12><たり:.*><.*>*<.*:Vconj|.*:Vstem2|.*:Vstem12><たり:.*><する:.*>}
	TARI~TARI: {<NP.*|.*:ADJ-NA|.*:ADJ-I><E-cPASTp>?<たり:.*><、:.*>?<NP.*|.*:ADJ-NA|.*:ADJ-I><E-cPASTp>?<たり:.*>}

 	V-pYOU_NI_SURU: {<.*:Vindef><E-cPRESn><NP-YOU><に:.*><し:.*><E-p.*>}
 	V-cYOU_NI_SURU: {<.*:Vindef><E-cPRESn><NP-YOU><に:.*><し:.*><E-c.*>}
 	V-cYOU_NI_SURU: {<.*:Vindef><E-cPRESn><NP-YOU><に:.*><する:.*><E-p.*>}
 	V-pYOU_NI_SURU: {<.*:Vdict><NP-YOU><に:.*><し:.*><E-p.*>}
 	V-cYOU_NI_SURU: {<.*:Vdict><NP-YOU><に:.*><し:.*><E-c.*>}
 	V-cYOU_NI_SURU: {<.*:Vdict><NP-YOU><に:.*><する:.*>}

    NI_SHITE_WA: {<NP.*><に:.*><し:.*><E-cTEp><は:.*>}

 	V-pKOTO_NI_SURU: {<NP-KOTO1.*><に:.*><し:.*><E-p.*>}
 	V-cKOTO_NI_SURU: {<NP-KOTO1.*><に:.*><し:.*><E-c.*>}
 	V-cKOTO_NI_SURU: {<NP-KOTO1.*><に:.*><する:.*>}

    NI_SHITATTE: {<V-cPRESp|A-.*|NP.*><に:.*><V-SHITATTE>}
    NI_SHITATTE: {<V-cPRESp|A-.*|NP.*><に:.*><V-SHITA><NP-TOKORO><E-cTEp>}


    TO_SHITATTE: {<V-.*|A-.*|NP.*><と:.*><V-SHITATTE>}
    TO_SHITATTE: {<V-.*|A-.*|NP.*><と:.*><V-SHITA><NP-TOKORO><E-cTEp>}

 	V-pNI_SURU1: {<NP.*><に:.*><し:.*><E-p.*>}
 	V-cNI_SURU1: {<NP.*><に:.*><し:.*><E-c.*>}
  	V-cNI_SURU1: {<NP.*><に:.*><する:.*>}

 	V-pNI_SURU2: {<.*:ADJ-NA><に:.*><し:.*><E-p.*>}
 	V-cNI_SURU2: {<.*:ADJ-NA><に:.*><し:.*><E-c.*>}
  	V-cNI_SURU2: {<.*:ADJ-NA><に:.*><する:.*>}

 	V-pGA_SURU: {<NP.*><が:.*><し:.*><E-p.*>}
 	V-cGA_SURU: {<NP.*><が:.*><し:.*><E-c.*>}
  	V-cGA_SURU: {<NP.*><が:.*><する:.*>}

 	V-pKU_SURU: {<.*:ADJ-I><し:.*><E-p.*>}
 	V-cKU_SURU: {<.*:ADJ-I><し:.*><E-c.*>}
  	V-cKU_SURU: {<.*:ADJ-I><する:.*>}

    V-pFURI_O_SURU: {<.*:V.*><E-c.*>?<NP-FURI><を:.*><し:.*><E-p.*>}
    V-pFURI_O_SURU: {<.*:ADJ-I><NP-FURI><を:.*><し:.*><E-p.*>}
    V-pFURI_O_SURU: {<.*:ADJ-NA><な:.*><NP-FURI><を:.*><し:.*><E-p.*>}
    V-pFURI_O_SURU: {<NP.*><の:.*><NP-FURI><を:.*><し:.*><E-p.*>}

    V-cFURI_O_SURU: {<.*:V.*><E-c.*>?<NP-FURI><を:.*><し:.*><E-c.*>}
    V-cFURI_O_SURU: {<.*:ADJ-I><NP-FURI><を:.*><し:.*><E-c.*>}
    V-cFURI_O_SURU: {<.*:ADJ-NA><な:.*><NP-FURI><を:.*><し:.*><E-c.*>}
    V-cFURI_O_SURU: {<NP.*><の:.*><NP-FURI><を:.*><し:.*><E-c.*>}

    V-cFURI_O_SURU: {<.*:V.*><E-c.*>?<><NP-FURI><を:.*><する:.*>}
    V-cFURI_O_SURU: {<.*:ADJ-I><NP-FURI><を:.*><する:.*>}
    V-cFURI_O_SURU: {<.*:ADJ-NA><な:.*><NP-FURI><を:.*><する:.*>}
    V-cFURI_O_SURU: {<NP.*><の:.*><NP-FURI><を:.*><する:.*>}

 	KUSE_SHITE: {<.*:Vdict|.*:ADJ-I><NP-KUSE><し:.*><E-cTEp>}
 	KUSE_SHITE: {<.*:ADJ-NA><な.*><NP-KUSE><し:.*><E-cTEp>}
 	KUSE_SHITE: {<NP.*><の.*><NP-KUSE><し:.*><E-cTEp>}

 	V-pMONO_TO_SURU: {<.*:V.*><E-c.*>?<NP-MONO><と:.*><し:.*><E-pTEp>}
 	V-cMONO_TO_SURU: {<.*:V.*><E-c.*>?<NP-MONO><と:.*><し:.*><E-cTEp>}
 	V-cMONO_TO_SURU: {<.*:V.*><E-c.*>?<NP-MONO><と:.*><する:.*>}


    NI_SHITE_MO: {<.*:V.*><E-c.*>?<に:.*><し:.*><E-cTEp><も:.*>}
    NI_SHITE_MO: {<.*:ADJ-I><に:.*><し:.*><E-cTEp><も:.*>}
 	NI_SHITE_MO: {<NP.*|.*:ADJ-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)?<に:.*><し:.*><E-cTEp><も:.*>}

	NI_SHITEMO~NI_SHITEMO: {<NI_SHITE_MO><.*>*<NI_SHITE_MO>}



#DEKIRU
  	V-pKOTO_GA_DEKIRU: {<NP-KOTO1pres><が:.*><V-p.*DEKIRU>}
  	V-cKOTO_GA_DEKIRU: {<NP-KOTO1pres><が:.*><V-c.*DEKIRU>}


#MIERU
	V-pNI_MIERU: {<.*:Vindef><E-cTEn><に:.*><見え:.*|みえ:.*><E-p.*>}
	V-pNI_MIERU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><に:.*><見え:.*|みえ:.*><E-p.*>}
	V-pNI_MIERU: {<NP.*|.*:ADJ-I|.*:ADJ-NA><に:.*><見え:.*|みえ:.*><E-p.*>}
	V-cNI_MIERU: {<.*:Vindef><E-cTEn><に:.*><見え:.*|みえ:.*><E-c.*>}
	V-cNI_MIERU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><に:.*><見え:.*|みえ:.*><E-c.*>}
	V-cNI_MIERU: {<NP.*|.*:ADJ-I|.*:ADJ-NA><に:.*><見え:.*|みえ:.*><E-c*>}
	V-cNI_MIERU: {<.*:Vindef><E-cTEn><に:.*><見える:.*|みえる:.*>}
	V-cNI_MIERU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><に:.*><見える:.*|みえる:.*>}
	V-cNI_MIERU: {<NP.*|.*:ADJ-I|.*:ADJ-NA><に:.*><見える:.*|みえる:.*>}

#---------- TE & TEIRU
	V-pGARU/GATTEIRU: {<.*:ADJ-I|.*:ADJ-NA><がり:.*><E-p.*>}
	V-cGARU/GATTEIRU: {<.*:ADJ-I|.*:ADJ-NA><がら:.*><E-c.*n>}
	V-cGARU/GATTEIRU: {<.*:ADJ-I|.*:ADJ-NA><がっ:.*><E-cPASTp>}
	V-pGARU/GATTEIRU: {<.*:ADJ-I|.*:ADJ-NA><がっ:.*><E-cTEp><V-p.*IRUx>}
	V-cGARU/GATTEIRU: {<.*:ADJ-I|.*:ADJ-NA><がっ:.*><E-cTEp><V-c.*IRUx>}
	V-cGARU/GATTEIRU: {<.*:ADJ-I|.*:ADJ-NA><がる:.*>}

 	V-pKOTO_NI_NATTEIRU: {<.*:Vdict|NP.*><NP-KOTO><に:.*><なっ:.*><E-cTEp><V-p.*IRUx>}
 	V-cKOTO_NI_NATTEIRU: {<.*:Vdict|NP.*><NP-KOTO><に:.*><なっ:.*><E-cTEp><V-c.*IRUx>}
 	V-pKOTO_NI_NATTEIRU: {<.*:Vindef><E-cPRESn><NP-KOTO><に:.*><なっ:.*><E-cTEp><V-p.*IRUx>}
 	V-cKOTO_NI_NATTEIRU: {<.*:Vindef><E-cPRESn><NP-KOTO><に:.*><なっ:.*><E-cTEp><V-c.*IRUx>}



 	V-pTEIRU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><V-p.*IRUx>}								# teimasu, teimasen, teimashita, teimasen deshita
 	V-cTEITA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><い:.*><E-.*PASTp>}						# teita
 	V-cTEIRU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp><V-c.*IRUx>}								# teiru

	V-TEn: {<.*:Vindef><E-cTEn>}																# naide
	V-TEp: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cTEp>}											# te
	V-TEp: {<.*:Vstem1|.*:Vstem12><たく:助動詞><E-cTEp>}											# te
	V-TEp: {<くれ:.*><E-cTEp>}

    V-pTE_IKU: {<V-TE.*><いき:.*|行き:.*><E-p.*>}
    V-cTE_IKU: {<V-TE.*><いっ:.*|行っ:.*><E-cPASTp>}
    V-cTE_IKU: {<V-TE.*><いか:.*|行か:.*><E-cPRESn>}
    V-cTE_IKU: {<V-TE.*><いく:.*|行く:.*>}


#ARU
    YORI_HOKA_NAI: {<.*:Vdict><より:.*>?<NP-HOKA><は:.*>?<ない:.*>}
    YORI_HOKA_NAI: {<.*:Vdict><より:.*>?<NP-HOKA><NP-SHIKATTA><が:.*>?<ない:.*>}

    TE_SHOU_GA_NAI/TE_SHIKATA_GA_NAI: {<V-TEp><も:.*>?<NP-SHOUGA|NP-SHIKATA><が:.*>?<V-.*nARUx>}

 	HAZU_GA_NAI: {<.*:Vdict><NP-HAZU><が:.*><V-.*nARUx>}
 	HAZU_GA_NAI: {<.*:ADJ-NA><な:.*><NP-HAZU><が:.*><V-.*nARUx>}
 	HAZU_GA_NAI: {<.*:ADJ-Idict><NP-HAZU><が:.*><V-.*nARUx>}
  	HAZU_GA_NAI: {<NP.*><の:.*><NP-HAZU><が:.*><V-.*nARUx>}

 	HAZU_DA: {<.*:Vdict><NP-HAZU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
 	HAZU_DA: {<.*:ADJ-NA><な:.*><NP-HAZU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
 	HAZU_DA: {<.*:ADJ-Idict><NP-HAZU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
  	HAZU_DA: {<NP.*><の:.*><NP-HAZU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}

 	HITSUYOU_GA_ARU: {<.*:Vdict><必要:.*><が:.*><V-.*ARUx>}

	TSUTSU_ARU: {<.*:Vstem1|.*:Vstem12><つつ:.*><V-.*ARUx>}
	TSUTSU: {<.*:Vstem1|.*:Vstem12><つつ:.*><も:.*>?}

	V-pDAKE_NO_KOTO_WA_ARU: {<だけ:.*><の:.*><NP-KOTO><は:.*><V-p.*ARUx>}
	V-cDAKE_NO_KOTO_WA_ARU: {<だけ:.*><の:.*><NP-KOTO><は:.*><V-c.*ARUx>}
	V-pDAKE_NO_KOTO_WA_ARU: {<NP-DAKE><の:.*><NP-KOTO><は:.*><V-p.*ARUx>}
	V-cDAKE_NO_KOTO_WA_ARU: {<NP-DAKE><の:.*><NP-KOTO><は:.*><V-c.*ARUx>}

  	V-pTA_KOTO_GA_ARU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><NP-KOTO><が:.*><V-p.*ARUx>}
  	V-cTA_KOTO_GA_ARU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><NP-KOTO><が:.*><V-c.*ARUx>}

  	V-pKOTO_GA_ARU: {<NP-KOTO1pres><が:.*><V-p.*ARUx>}
  	V-cKOTO_GA_ARU: {<NP-KOTO1pres><が:.*><V-c.*ARUx>}
  	V-pKOTO_GA_ARU: {<.*:Vindef><E-cPRESn><NP-KOTO><が:.*><V-p.*ARUx>}
  	V-cKOTO_GA_ARU: {<.*:Vindef><E-cPRESn><NP-KOTO><が:.*><V-c.*ARUx>}
  	V-pKOTO_GA_ARU: {<.*:Vdict><NP-KOTO><が:.*><V-p.*ARUx>}
  	V-cKOTO_GA_ARU: {<.*:Vdict><NP-KOTO><が:.*><V-c.*ARUx>}


	V-pKAI_GA_ARU: {<.*:Vstem1|.*:Vstem12><NP-KAI><が:.*><V-p.*ARUx>}
	V-pKAI_GA_ARU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><NP-KAI><が:.*><V-p.*ARUx>}
	V-pKAI_GA_ARU: {<NP.*><の:.*><NP-KAI><が:.*><V-p.*ARUx>}
	V-cKAI_GA_ARU: {<.*:Vstem1|.*:Vstem12><NP-KAI><が:.*><V-c.*ARUx>}
	V-cKAI_GA_ARU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><NP-KAI><が:.*><V-c.*ARUx>}
	V-cKAI_GA_ARU: {<NP.*><の:.*><NP-KAI><が:.*><V-c.*ARUx>}



  	V-pGA_ARU: {<が:.*><.*:ADV|NP.*>?<V-p.*ARUx>}
 	V-cGA_ARU: {<が:.*><.*:ADV|NP.*>?<V-c.*ARUx>}

  	V-pTE_ARU: {<V-TE.*><V-p.*ARUx>}
 	V-cTE_ARU: {<V-TE.*><V-c.*ARUx>}


#IRU
 	V-pGA_IRU: {<が:.*><.*:ADV|NP.*>?<V-p.*IRUx>}
 	V-cGA_IRU: {<が:.*><.*:ADV|NP.*>?<V-c.*IRUx>}

 	V-pTE_BAKARI_IRU: {<V-TEp><ばかり:.*><V-p.*IRUx>}
 	V-cTE_BAKARI_IRU: {<V-TEp><ばかり:.*><V-c.*IRUx>}

	V-pTO_IWARETE_IRU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><と:.*><言わ:.*><V-pTEIRU>}
	V-cTO_IWARETE_IRU: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><と:.*><言わ:.*><V-cTEIRU>}
	V-pTO_IWARETE_IRU: {<.*:ADJ-Idict><と:.*><言わ:.*><V-pTEIRU>}
	V-cTO_IWARETE_IRU: {<.*:ADJ-Idict><と:.*><言わ:.*><V-cTEIRU>}
	V-pTO_IWARETE_IRU: {<NP.*|.*:ADJ-NA><E-cPASTp><と:.*><言わ:.*><V-pTEIRU>}
	V-cTO_IWARETE_IRU: {<NP.*|.*:ADJ-NA><E-cPASTp><と:.*><言わ:.*><V-cTEIRU>}



#TE
    NAKU_TEMO_II: {<V-TEn><も:.*><いい:.*>}

	TE_WA_IKENAI: {<V-TEp><は:.*><いけ:.*><E-.*n>}
    TE_KUDASAI: {<V-TEp><ください:.*|下さい:.*>}
    TE_GORAN: {<V-TEp><NP-GORAN><なさい>?}
	TE_KARA_DE_NAI_TO: {<V-TEp><から:.*><.*:DE><E-cPRESn><と:.*><ば:.*>}
	TE_KARA_DE_NAI_TO: {<V-TEp><から:.*><.*:DE>}
    TE_KARA: {<V-TEp><から:.*>}
    TEMO_II_DESU: {<V-TEp><も:.*><いい:.*>}
    TEMO_II_DESU: {<.*:ADJ-I><て:.*><も:.*><いい:.*>}
    TEMO_II_DESU: {<NP.*|.*:ADJ-NA><でも:.*><いい:.*>}
    TE_HOSHII: {<V-TE.*><欲しい:.*|ほしい:.*>}
    TE_SUMIMASEN: {<V-TE.*><すみません:.*>}
    TE_YOKATTA: {<V-TE.*><よかっ:.*><E-cPASTp>}
    TEIRU_TOKORO: {<V-cTEIRU><NP-TOKORO>}
    TEIRU_BAAI_JANAI: {<V-cTEIRU><NP-BAAI><じゃ:.*><E-.*n>}

#IKENAI
	CHA_IKENAI/JA_IKENAI: {<.*:Vconj|.*:Vstem2|.*:Vstem12><ちゃ:.*|じゃ:.*><だめ:.*|ダメ:.*>}
	CHA_IKENAI/JA_IKENAI: {<.*:Vconj|.*:Vstem2|.*:Vstem12><ちゃ:.*|じゃ:.*><いけ:.*><E-.*n>}
    
    NAKEREBA_IKENAI: {<.*:Vindef><E-cPRESn><ば:.*><いけ:.*><E-.*n>}
    NAKEREBA_IKENAI: {<.*:Vindef><E-cPRESn><ば:.*><いけ:.*><E-.*n>}

    NAKUTE_WA_IKENAI: {<V-TEn><は:.*><いけ:.*><E-.*n>}

    TE_WA_IKENAI_KARA: {<.*:Vindef><E-cTEn><は:.*><いけ:.*><E-cPRESn><から:.*>}
    TE_WA_IKENAI_KARA: {<.*:Vdict><と:.*><いけ:.*><E-cPRESn><から:.*>}

    NAITO_IKENAI: {<.*:Vindef><E-cPRESn><と:.*><いけ:.*><E-.*n>}
    NAITO_IKENAI: {<.*:Vindef><E-cPRESn><と:.*><くだめ:.*|ダメ:.*>}

#NARANAI
	NEBA_NARANAI: {<.*:Vindef><ね:.*><ば:.*><V-.*nNARU>}

	NI_HOKA_NARANAI: {<NP.*><に:.*><ほかなり:.*><E-p.*n>}
	NI_HOKA_NARANAI: {<NP.*><に:.*><ほかなら:.*><E-c.*n>}

    NAKUTE_WA_NARANAI: {<V-TEn><は:.*><V-.*nNARU>}

    NAKEREBA_NARANAI: {<.*:Vindef><E-cPRESn><ば:.*><V-.*nNARU>}

    NAKUCHA: {<.*:Vindef><E-cPRESn><ちゃ:.*><いけ:.*|なら:.*><E-c.*n>}
    NAKUCHA: {<.*:Vindef><E-cPRESn><ちゃ:.*><いけ:.*|なり:.*><E-p.*n>}
    NAKUCHA: {<.*:Vindef><E-cPRESn><ちゃ:.*><ダメ:.*>?}

#SUMU
	NAKUTE_SUMU: {<V-TEn><V-.*SUMU>}

    TE_SUMU: {<V-TEp><V-.*SUMU>}
    TE_SUMU: {<NP.*|.*:ADJ-NA><E-cTEp><V-.*SUMU>}
    TE_SUMU: {<.*:ADJ-I><E-cTEp><V-.*SUMU>}



	GA_HOSHII: {<が:.*><.*>?<ほしい:.*|欲しい:.*>}
	GA_HITSUYOU: {<NP.*><は:.*|が:.*><必要:.*>}

    TARA_II_DESU_KA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><.*:TARA><いい:.*><です:.*><か:.*>}
 	WA_DOU_DESU_KA: {<NP.*><は:.*><どう:.*><です:.*><か:.*>}

 	DE_SHIKANAI: {<NP.*><E-cTEp><しか:.*><ない:.*|V-c.*nARUx>}
 	SHIKANAI: {<.*:Vdict><しか:.*><ない:.*|V-c.*nARUx>}

 	GA_HAYAI_KA: {<.*:Vdict><が:.*><早い:.*><か:.*>}

    NI_KATAKUNAI: {<.*:Vdict><に:.*><かたく:.*><E-cPRESn>}

    NIWA_OYOBANAI: {<.*:Vdict|NP.*><に:.*><は:.*>?<及ば:.*><E-cPRESn>}

    TOMO_NARU_TO/TOMO_NAREBA: {<.*:Vdict|NP.*><と:.*><も:.*>?<V-c.*NARU><と:.*>}
    TOMO_NARU_TO/TOMO_NAREBA: {<.*:Vdict|NP.*><と:.*><も:.*>?<なれ:.*><ば:.*>}

  	V-pTO_MIRARERU: {<NP.*|.*:Vdict|.*:ADJ-.*><と:.*><み:.*><V-pTEIRU>}
  	V-cTO_MIRARERU: {<NP.*|.*:Vdict|.*:ADJ-.*><と:.*><み:.*><V-cTEIRU>}
  	V-pTO_MIRARERU: {<NP.*|.*:Vdict|.*:ADJ-.*><と:.*><み:.*><られ:.*><E-p.*>}
  	V-cTO_MIRARERU: {<NP.*|.*:Vdict|.*:ADJ-.*><と:.*><み:.*><られ:.*><E-c.*>}
  	V-cTO_MIRARERU: {<NP.*|.*:Vdict|.*:ADJ-.*><と:.*><み:.*><られる:.*>}

    NU: {<.*:Vindef><ぬ:.*>}
    PPANASHI: {<.*:Vstem1|.*:Vstem12><NP-PPANASHI>}
    PPOI: {<.*:Vstem1|.*:Vstem12|.*:ADJ-I|NP.*><っぽい:.*>}


    TE_YARU: {<V-TEp><やる:.*>}
    TE_YARU: {<V-TEp><やら:.*><E-cPRESn>}

    V-pNI_KAGIRU: {<.*:V.*><E-cPRES.*>?<に:.*><限り:.*><E-p.*>}
    V-pNI_KAGIRU: {<NP.*><に:.*><限り:.*><E-p.*>}
    V-cNI_KAGIRU: {<.*:V.*><E-cPRES.*>?<に:.*><限ら:.*><E-cPRESn>}
    V-cNI_KAGIRU: {<NP.*><に:.*><限ら:.*><E-cPRESn>}
    V-cNI_KAGIRU: {<.*:V.*><E-cPRES.*>?<に:.*><限っ:.*><E-cPASTp>}
    V-cNI_KAGIRU: {<NP.*><に:.*><限っ:.*><E-cPASTp>}
    V-cNI_KAGIRU: {<.*:V.*><E-cPRES.*>?<に:.*><限る:.*>}
    V-cNI_KAGIRU: {<NP.*><に:.*><限る:.*>}


# ------------------ AP
	GE: {<A-NA|A-I|NP.*|.*:Vstem1|.*:Vstem12><NP-GE|たげ:.*>}
	A-cBA: {<.*:ADJ-I><ば:.*>}
	A-cBA: {<.*:ADJ-I><E-cPRESn><ば:.*>}
	A-cBA: {<.*:ADJ-NA><なら:.*><ば:.*>}
	A-cBA: {<.*:ADJ-NA><じゃ:.*|.*:DE><E-cPRESn><ば:.*>}

	A-NORMnai: {<ない:ADJ-Idict>}
	A-NORMnaku: {<なく:.*>}
	A-NORMii: {<いい:ADJ-Idict>}
	A-NORMshiganai: {<しがない:.*>}
	A-Idict: {<.*:ADJ-Idict>}
	A-I: {<.*:ADJ-I>}
	A-NORMyokatta: {<よかっ:.*><E-cPASTp>}
	A-NORM: {<A-I|A-i.*><E-cPRESn|E-cPASTn|E-cPASTp>}									# i, ta, kunai, kunakatta
	A-NORM: {<.*:ADJ-NA><じゃ:.*><E-cPRESn|E-cPASTn>}									# janakatta, janai, kunai
	A-NORM: {<.*:ADJ-NA><E-cPASTdattap><E-cPASTp>}										# datta
	A-NA: {<.*:ADJ-NA>}																	# na

	DAROU: {<.*:Vdict><NP-N|NP-NO>?<E-cPAST.*><う:.*>}
	DAROU: {<A-.*><NP-N|NP-NO>?<E-cPAST.*><う:.*>}
	DAROU: {<NP.*><な:.*>?<NP-N|NP-NO>?<E-cPAST.*><う:.*>}
	DAROU: {<そう:.*><NP-N|NP-NO>?<E-cPAST.*><う:.*>}


    NOMINARAZU: {<NP.*|.*:Vdict|A-NORM.*|A-I><のみ:.*><なら:.*><ず:.*>}
    NOMINARAZU: {<A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<のみ:.*><なら:.*><ず:.*>}

    V-pNI_ATARANAI: {<.*:Vdict><に:.*><は:.*>?<あたり:.*><E-p.*n>}
    V-cNI_ATARANAI: {<.*:Vdict><に:.*><は:.*>?<あたら:.*><E-c.*n>}

    ZARU: {<.*:Vindef><ざる:.*>}
 	ZARU_O_ENAI: {<.*:Vindef|せ:.*><ざる:.*><を:.*><得:.*><E-.*>}

 	ZU_TOMO: {<.*:Vindef><ず:.*><と:.*><も:.*>}
 	ZU_JIMAI: {<.*:Vindef|せ:.*><ず:.*><NP-JIMAI>}
 	ZU_NI_SUMU: {<.*:Vindef|せ:.*><ず:.*><に:.*><V-.*SUMU>}
 	NAI_DEWA_IRARENAI: {<V-TEn><は:.*><い:.*><られ:.*><E-.*n>}
 	TEWA_IRARENAI: {<V-TEp><は:.*><い:.*><られ:.*><E-.*n>}
 	TEWA~TEWA: {<V-TEp><は:.*><.*:Vstem1|.*:Vstem12|V-TEp><V-TEp><は:.*><.*:Vstem1|.*:Vstem12|V-TEp>}
 	TE_WA_IRARENAI: {<NP.*|A-NA><E-cTEp><は:.*><い:.*><られ:.*><E-.*n>}
 	TEWA/DEWA: {<V-TEp><は:.*>}
 	TEWA/DEWA: {<NP.*|A-NA|A-I><E-cTEp><は:.*>}
 	ZUNI_WA_IRARENAI: {<.*:Vindef><ず:.*><に:.*><は:.*><い:.*><られ:.*><E-.*n>}
 	ZUNI: {<.*:Vindef><ず:.*><に:.*>?}
 	ZUNI: {<せ:.*><ず:.*><に:.*>?}

 	TEMO_HAJIMARANAI: {<V-TEp><も:.*><始まら:.*><E-.*n>}
 	TEMO_KAMAWANAI: {<V-TEp><も:.*><かまわ:.*|構わ:.*><E-.*n>}
 	TEMO_KAMAWANAI: {<NP.*|A-NA><でも:.*><かまわ:.*|構わ:.*><E-.*n>}
 	TEMO_KAMAWANAI: {<NP.*|A-NA><で:.*><も:.*><かまわ:.*|構わ:.*><E-.*n>}
 	TEMO_KAMAWANAI: {<A-I><E-cTEp><も:.*><かまわ:.*|構わ:.*><E-.*n>}
 	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<V-TEp><も:.*><NP-SHOUGA><E-.*n|V-.*nARUx|A-NORMnai>}
  	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<V-TEp><も:.*><NP-SHIKATTA><が:.*><E-.*n|V-.*nARUx|A-NORMnai>}
 	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<A-NA><でも:.*><NP-SHOUGA><E-cPRESn|V-.*nARUx|A-NORMnai>}
  	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<A-NA><でも:.*><NP-SHIKATTA><が:.*><E-.*n|V-.*nARUx|A-NORMnai>}
 	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<A-NA><で:.*><も:.*><NP-SHOUGA><E-.*n|V-.*nARUx|A-NORMnai>}
  	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<A-NA><で:.*><も:.*><NP-SHIKATTA><が:.*><A-NORMnai>}
 	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<A-I><E-cTEp><も:.*><NP-SHOUGA><E-.*n|V-.*nARUx|A-NORMnai>}
  	TEMO_SHOU_GA_NAI/TEMO_SHIKATTA_GA_NAI: {<A-I><E-cTEp><も:.*><NP-SHIKATTA><が:.*><E-.*n|V-.*nARUx|A-NORMnai>}

	TO_KANGAERARERU: {<と:.*><考え:.*><られる:.*>}
	TO_KANGAERARERU: {<と:.*><考え:.*><られ:.*><E-pPRESp>}
	TO_KANGAERARERU: {<と:.*><考え:.*><V-pTEIRU>}


	TOKORO_O_MIRU_TO: {<TEIRU_TOKORO><を:.*><みる:.*|見る:.*><と:.*>}
	TOKORO_O_MIRU_TO: {<.*:V.*><E-c.*><NP-TOKORO><を:.*><みる:.*|見る:.*><と:.*>}

    TO_MIRU_TO: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><と:.*><みる:.*><と:.*>}
    TO_MIRU_TO: {<V-SHITA><と:.*><みる:.*><と:.*>}
    TO_MIRU_TO: {<.*:Vindef><E-c.*n><と:.*><みる:.*><と:.*>}
    TO_MIRU_TO: {<.*:Vdict><と:.*><みる:.*><と:.*>}
    TO_MIRU_TO: {<A-NA|A-NORM.*|A-Idict><と:.*><みる:.*><と:.*>}
    TO_MIRU_TO: {<NP.*><E-cPASTp><と:.*><みる:.*><と:.*>}

    TO_MIRU_YA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp><と:.*><みる:.*><や:.*>}
    TO_MIRU_YA: {<V-SHITA><と:.*><みる:.*><や:.*>}
    TO_MIRU_YA: {<.*:Vindef><E-c.*n><と:.*><みる:.*><や:.*>}
    TO_MIRU_YA: {<.*:Vdict><と:.*><みる:.*><や:.*>}

 	YORI: {<より:.*><A-.*>}
  	WA~YORI~DESU: {<NP.*><は:.*><NP.*><YORI>}


    KATA: {<.*:Vstem1|.*:Vstem12><かた:.*|方:.*>}
    NAGARA_MO: {<.*:Vstem1|.*:Vstem12><ながら:.*><も:.*>}
    NAGARA_MO: {<NP.*|A-Idict|A-NA|V-TEp><ながら:.*><も:.*>?}
    NAGARA: {<.*:Vstem1|.*:Vstem12><ながら:.*>}
    V-cNASAI:	{<.*:Vstem1|.*:Vstem12><なさい:.*>}
    KKONAI: {<.*:Vstem1|.*:Vstem12><っ:.*><こ:.*><E-cPRESn>}
    KKONAI: {<.*:Vindef><られ:.*><っ:.*><こ:.*><E-cPRESn>}
    MAI: {<.*:Vstem1|.*:Vstem12|.*:Vdict><まい:.*>}
    MAI: {<せ:.*|こ:.*><まい:.*>}

# ------------------ VP
 	V-IKOU_KEI: {<.*:Vjo><う:.*>}

 	V-pYOU_TO_SURU: {<V-IKOU_KEI><と:.*><し:.*><E-p.*p>}
 	V-cYOU_TO_SURU: {<V-IKOU_KEI><と:.*><し:.*><E-c.*p|.*:TARA>}
 	V-cYOU_TO_SURU: {<V-IKOU_KEI><と:.*><する:.*>}

 	V-pYOU_TO_SHINAI: {<V-IKOU_KEI><と:.*><し:.*><E-p.*n>}
 	V-cYOU_TO_SHINAI: {<V-IKOU_KEI><と:.*><し:.*><E-c.*n>}	

 	TO_AREBA:{<V-c.*|A-.*|NP.*><と:.*><あれ:.*><ば:.*>}


 	V-cBA: {<.*:Vba><ば:.*>}
 	V-cBA: {<.*:Vindef><E-cPRESn><ば:.*>}

 	V-TARA: {<.*:Vconj|.*:Vstem2|.*:Vstem12><.*:TARA>}									# tara

 	V-pSASERARERU: {<.*:Vindef><させ:.*|せ:.*><られ:.*><E-p.*>}
 	V-cSASERARERU: {<.*:Vindef><させ:.*|せ:.*><られ:.*><E-c.*>}
 	V-cSASERARERU: {<.*:Vindef><させ:.*|せ:.*><られる:.*>}

 	V-pRARERU: {<.*:Vindef><られ:.*><E-p.*>}
 	V-cRARERU: {<.*:Vindef><られる:.*>}
 	V-cRARERU: {<やれる:.*|できる:.*|こられる:.*>}
 	V-cRARERU: {<.*:Vindef><られ:.*><E-c.*>}

  	V-pSASERU: {<.*:Vindef><させ:.*|せ:.*><E-p.*>}
  	V-cSASERU: {<.*:Vindef><させ:.*|せ:.*><E-c.*>}
 	V-cSASERU: {<.*:Vindef><せる:.*>}


 	V-pTO_KIITA: {<と:.*><聞き:.*|きき:.*><E-pPASTp>}					
 	V-cTO_KIITA: {<と:.*><聞い:.*|きい:.*><E-cPASTp>}

 	V-SHITA: {<し:Vstem12><E-cPASTp>}

	V-pPASTp: {<.*:Vstem1|.*:Vstem12><E-pPASTp>}										# mashita
	V-pPASTn: {<.*:Vstem1|.*:Vstem12><E-pPASTn>}										# masen deshita
	V-pPRESn: {<.*:Vstem1|.*:Vstem12><E-pPRESn>}										# masen
	V-pPRESp: {<.*:Vstem1|.*:Vstem12><E-pPRESp>}										# masu

	V-cPASTp: {<.*:Vconj|.*:Vstem2|.*:Vstem12><E-cPASTp>}								# ta
	V-cPASTp: {<V-SHITA>}																# ta
	V-cPASTn: {<.*:Vindef><E-cPASTn>}													# nakatta
	V-cPRESn: {<.*:Vindef><E-cPRESn>}													# nai
	V-cPRESN: {<NU>}
	V-cPRESp: {<.*:Vdict>}																# ku/ru/bu/

 	V-pTAI: {<.*:Vstem1|.*:Vstem12><たかっ:.*><E-cPASTp>}								# takatta
 	V-cTAI: {<.*:Vstem1|.*:Vstem12><たく:.*><E-cPASTn>}									# tanakatta
 	V-cTAI: {<.*:Vstem1|.*:Vstem12><たく:.*><E-cPRESn>}									# takunai
 	V-cTAI: {<.*:Vstem1|.*:Vstem12><たい:.*>}											# tai
 	
 	SONNA_NI: {<そんなに:.*><V-.*|A-NA|A-NORM|A-Idict>}

 	YOTEI_DA: {<V-cPRESp.*><NP-YOTEI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	YOTEI_DA: {<NP.*><NP-YOTEI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}


 	V-pYOU_TO_OMOU: {<V-IKOU_KEI><と:.*><V-p.*OMOU>}				
 	V-cYOU_TO_OMOU: {<V-IKOU_KEI><と:.*><V-c.*OMOU>}

 	V-pTO_OMOU: {<V-.*><と:.*><V-p.*OMOU>}				
 	V-cTO_OMOU: {<V-.*><と:.*><V-c.*OMOU>}
 	V-pTO_OMOU: {<NP.*|A-NA><E-cPASTp><と:.*><V-p.*OMOU>}					
 	V-cTO_OMOU: {<NP.*|A-NA><E-cPASTp><と:.*><V-c.*OMOU>}
 	V-pTO_OMOU: {<A-NORM.*|A-Idict><と:.*><V-p.*OMOU>}						
 	V-cTO_OMOU: {<A-NORM.*|A-Idict><と:.*><V-c.*OMOU>}


   	V-pNI_KI_GA_TSUKU: {<V-c.*><に:.*><NP-KOTO><気がつく:.*|気が付き:.*><E-p.*>}
 	V-cNI_KI_GA_TSUKU: {<V-c.*><に:.*><NP-KOTO><気がつく:.*|気が付い:.*><E-cPASTp>}
 	V-cNI_KI_GA_TSUKU: {<V-c.*><に:.*><NP-KOTO><気がつく:.*|気が付か:.*><E-cPRESn>}
 	V-cNI_KI_GA_TSUKU: {<V-c.*><に:.*><NP-KOTO><気がつく:.*|気が付く:.*>}
 	V-cNI_KI_GA_TSUKU: {<NP.*><に:.*><気がつく:.*|気が付く:.*>}

##### SENTENCE 1st
	DONNA: {<どんな:.*><NP.*>}
 
    MADA: {<まだ:.*><NP.*>}
    MADA: {<まだ:.*><V-.*>}

    V-cSASUGA: {<さすが:.*><に:.*><V-c.*>}
    V-pSASUGA: {<さすが:.*><に:.*><V-p.*>}
    NP-SASUGA: {<さすが:.*><の:.*><NP.*>}

    SONNA_NI: {<そんなに:.*><V-.*>}


 	TO_IU_KOTO_DA: {<A-Idict|V-cPRESp.*><という:.*|との:.*|って:.*><NP-KOTO><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	TO_IU_KOTO_DA: {<NP.*|A-NA><E-cPASTp>?<という:.*|NP-TONO:.*|って><NP-KOTO><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	TO_IU_KOTO_DA: {<A-Idict|V-cPRESp.*><と:.*><の:.*><NP-KOTO><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	TO_IU_KOTO_DA: {<NP.*|A-NA><E-cPASTp>?<と:.*><の:.*><NP-KOTO><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
	TTE: {<NP.*><って:.*|っていう:.*>}

	TO_IU_NOWA: {<という:.*><NP-NO><は:.*>}

	V-pNIMO_HODO_GA_ARU: {<V-cPRESp|NOUN.*|A-.*><に:.*><も:.*><ほど:.*><V-p.*GA_ARU>}
	V-cNIMO_HODO_GA_ARU: {<V-cPRESp|NOUN.*|A-.*><に:.*><も:.*><ほど:.*><V-c.*GA_ARU>}


	V-pOSORE_GA_ARU: {<V-c.*><NP-OSORE><V-p.*GA_ARU>}
	V-cOSORE_GA_ARU: {<V-c.*><NP-OSORE><V-c.*GA_ARU>}
	V-pOSORE_GA_ARU: {<NP.*><の.*><NP-OSORE><V-p.*GA_ARU>}
	V-cOSORE_GA_ARU: {<NP.*><の.*><NP-OSORE><V-c.*GA_ARU>}

  	V-pTOKORO_GA_ARU: {<V-c.*><NP-TOKORO><V-p.*GA_ARU>}
  	V-pTOKORO_GA_ARU: {<A-NORM.*|A-Idict><NP-TOKORO><V-p.*GA_ARU>}
  	V-pTOKORO_GA_ARU: {<A-NA><な:.*><NP-TOKORO><V-p.*GA_ARU>}
  	V-pTOKORO_GA_ARU: {<NP.*><の:.*><NP-TOKORO><V-p.*GA_ARU>}
  	V-cTOKORO_GA_ARU: {<V-c.*><NP-TOKORO><V-c.*GA_ARU>}
  	V-cTOKORO_GA_ARU: {<A-NORM.*|A-Idict><NP-TOKORO><V-c.*GA_ARU>}
  	V-cTOKORO_GA_ARU: {<A-NA><な:.*><NP-TOKORO><V-c.*GA_ARU>}
  	V-cTOKORO_GA_ARU: {<NP.*><の:.*><NP-TOKORO><V-c.*GA_ARU>}

  	TE_KARA_TO_IU_MONO: {<TE_KARA><という:.*|TO-IU><NP-MONO>}
    TO_IU_MONO_DA: {<という:.*><NP-MONO><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    V-pTO_IU_MONO_DA: {<V-c.*|A-NORM.*|A-Idict><という:.*><NP-MONO><V-p.*GA_ARU>}
    V-cTO_IU_MONO_DA: {<V-c.*|A-NORM.*|A-Idict><という:.*><NP-MONO><V-c.*GA_ARU>}
    V-pTO_IU_MONO_DA: {<NP.*|A-NA><E-cPASTp>?<という:.*><NP-MONO><V-p.*GA_ARU>}
    V-cTO_IU_MONO_DA: {<NP.*|A-NA><E-cPASTp>?<という:.*><NP-MONO><V-c.*GA_ARU>}
 	TO_IU_MONO_DEWA_NAI: {<V-c.*|A-NORM.*|A-Idict><という:.*><NP-MONO><.*:DE><は:.*|も.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	TO_IU_MONO_DEWA_NAI: {<NP.*|A-NA><E-cPASTp>?<という:.*><NP-MONO><.*:DE><は:.*|も.*><E-cPRESn|V-.*nARUx|A-NORMnai>}




  	V-pMONO_GA_ARU: {<V-cPRES.*|A-NORM.*|A-Idict|A-NA><NP-MONO><V-p.*GA_ARU>}
  	V-cMONO_GA_ARU: {<V-cPRES.*|A-NORM.*|A-Idict|A-NA><NP-MONO><V-c.*GA_ARU>}
  	V-cMONO_DAKARA: {<V-c.*|A-NORM.*|A-Idict><NP-MONO|NP-MON><E-cPASTp><から:.*>}
  	V-cMONO_DAKARA: {<V-c.*|A-NORM.*|A-Idict><NP-MONO|NP-MON><です:.*><から:.*>}
  	V-cMONO_DAKARA: {<NP.*|A-NA><な:.*><NP-MONO|NP-MON><E-cPASTp><から:.*>}


 	DOKORO_DEWA_NAI: {<V-c.*|NP.*><NP-DOKORO><.*:DE><は:.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	DOKORO_KA: {<V-c.*|NP.*|A-NORM.*|A-Idict><どころか:.*>}
 	DOKORO_KA: {<A-NA><な:.*><どころか:.*>}

 	MONO_DEWA_NAI: {<V-c.*><NP-MONO><.*:DE><は:.*|も.*><E-cPRESn|V-.*nARUx|A-NORMnai>}

 	TO_IU_TOKORO_DA: {<NP.*><という:.*><NP-TOKORO><です:.*|.*:DE|E-cPASTdattap|でした:.*>}
 	TO_IU_WAKE_DEWA_NAI: {<NP.*|V-c.*|A-Idict|A-NORM.*><という:.*><NP-WAKE><.*:DE><は:.*|も.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	TO_IU_WAKE_DEWA_NAI: {<A-NA><E-cPASTp><という:.*><NP-WAKE><.*:DE><は:.*|も.*><E-cPRESn|V-.*nARUx|A-NORMnai>}

 	TO_IU_WAKE_DA: {<という:.*><NP-WAKE><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}

 	WAKE_DEWA_NAI: {<V-c.*|A-Idict|A-NORM.*><NP-WAKE><.*:DE><は:.*|も.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	WAKE_DEWA_NAI: {<A-NA><な:.*><NP-WAKE><.*:DE><は:.*|も.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	WAKE_GA_NAI: {<V-c.*|A-Idict|A-NORM.*><NP-WAKE><が:.*><E-.*n|V-.*nARUx|A-NORMnai>}
 	WAKE_GA_NAI: {<Np.*>((<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>))?<NP-WAKE><が:.*><E-.*n|V-.*nARUx|A-NORMnai>}
 	WAKE_GA_NAI: {<A-NA><な:.*><NP-WAKE><が:.*><E-.*n|V-.*nARUx|A-NORMnai>}
 	WAKE_DA: {<V-c.*|A-Idict|A-NORM.*><NP-WAKE><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	WAKE_DA: {<Np.*>((<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>))?<NP-WAKE><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	WAKE_DA: {<A-NA><な:.*><NP-WAKE><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}

 	NP-TO_IU_KOTO_: {<という:.*><NP-KOTO>}
  	NP-TO_IU_KOTO_: {<TO_IU><NP-KOTO>}

 	TO_IU_MONO: {<NP.*><という:.*><NP-MONO>}
 	TO_IU_MONO: {<NP.*><という:.*|TO_IU><NP-MONO>}


	ZUTSU: {<NP.*><ずつ:.*>}

##### SENTENCE 2nd
    ATO_DE: {<V-cPAST.*><NP-ATO|あと:.*><E-cPASTp*>}
    ATO_DE: {<NP.*><の:.*><NP-ATO|あと:.*><E-cPASTp>}
    ATO_DE: {<V-cPAST.*><あとで:.*>}
    ATO_DE: {<NP.*><の:.*><あとで:.*>}

    DANI: {<V-cPRESp|NP.*><だに:.*>}

    KARE~KARE: {<A-I><かれ:.*><A-I><かれ:.*>}

    KIRI: {<V-cPAST.*><NP-KIRI>}
    KIRI: {<NP.*><NP-KIRI>}

	KORO/GORO: {<NP.*><の:.*><NP-KORO>}		# Time
	KORO/GORO: {<V-c.*><NP-KORO>}
	KORO/GORO: {<A-.*><NP-KORO>}
	KORO/GORO: {<NP.*><NP-KORO>}			# NOUN

	KURAI_NARA: {<V-cPRESp.*><くらい:.*|ぐらい:.*><なら:.*>}

	KURAI/GURAI: {<V-c.*><くらい:.*|ぐらい:.*>}
	KURAI/GURAI: {<A-.*><な:.*><くらい:.*|ぐらい:.*>}
	KURAI/GURAI: {<NP.*><くらい:.*|ぐらい:.*>}

	MAMA_NI: {<V-cPRESp.*><が:.*>?<NP-MAMA><に:.*>?}
	MAMA_NI: {<V-cRARERU><が:.*>?<NP-MAMA><に:.*>?}
	MAMA_NI: {<NP.*><の:.*><NP-MAMA><に:.*>}
    MAMA: {<V-cPASTp.*><NP-MAMA>}
    MAMA: {<V-cPRESn><NP-MAMA>}
    MAMA: {<.*:ADJ-NA><な:.*><NP-MAMA>}
    MAMA: {<.*:ADJ-Idict><NP-MAMA>}
    MAMA: {<NP.*><の:.*><NP-MAMA>}

    MAE_NI: {<NP.*><の:.*><NP-MAE><に:.*>}
    MAE_NI: {<V-cPRESp.*><NP-MAE><に:.*>}

    MADE_NI: {<.*:Vdict><まで:.*><に:.*>}
    MADE_NI: {<NP.*><まで:.*><に:.*>}

    NAITO: {<V-cPRESn|A-NORM.*><と:.*>}
    NAITO: {<NP.*|A-NA><じゃ:.*|で:.*><E-cPRESn><と:.*>}


	NARI~NARI: {<V-cPRESp><なり:.*><V-cPRESp><なり:.*>}    
	NARI~NARI: {<NP.*><なり:.*><NP.*><なり:.*>}    


	NARI: {<V-cPRESp><なり:.*>}    

	ICHIBAN: {<NP-ICHIBAN><A-.*>}
	ICHIBAN: {<NP.*><は:.*|が:.*><NP-ICHIBAN><A-.*>}
	ICHIBAN: {<V-cPRESp.*><は:.*|が:.*><NP-ICHIBAN><A-.*>}

  	TOKI: {<A-NA><な:.*><NP-TOKI>}
 	TOKI: {<A-Idict><NP-TOKI>}
    TOKI: {<V-c.*><NP-TOKI>}
    TOKI: {<NP.*><の:.*><NP-TOKI>}

    TO_TOMO_NI: {<V-c.*|NP.*><と共に:.*>}


 	GARI: {<A-NA><がり:.*>}
 	GARI: {<A-NORM.*|A-I><がり:.*>}

 	NP-YA_: {<NP.*><や:.*><NP.*>}


##### SENTENCE middle
	AMARI_NI_MO: {<あまりに:.*><も:.*>?<NP.*|V-.*|A-.*>}
	AMARI_NI_MO: {<NP-AMARI><の:.*><NP.*>}
	AMARI: {<V-cPRESp.*><NP-AMARI>}
	AMARI: {<V-cPAST.*><NP-AMARI>}
	AMARI: {<NP.*><の:.*><NP-AMARI>}

    BAAI_WA: {<V-c.*><NP-BAAI><は:.*>}
    BAAI_WA: {<V-c.*><ば:.*><あい:.*><は:.*>}
    BAAI_WA: {<A-NA><な:.*><NP-BAAI><は:.*>}	
    BAAI_WA: {<A-Idict><NP-BAAI><は:.*>}														
    BAAI_WA: {<NP.*><の:.*><NP-BAAI><は:.*>}	
    BAAI_WA: {<A-NA><な:.*><ば:.*><あい:.*><は:.*>}
    BAAI_WA: {<A-Idict><ば:.*><あい:.*><は:.*>}														
    BAAI_WA: {<NP.*><の:.*><ば:.*><あい:.*><は:.*>}

    MADE_MO_NAI: {<V-cPRESp.*><まで:.*><も:.*><A-NORMnai>}
    BEKU_MO_NAI: {<V-cPRESp.*><べく:.*><も:.*><A-NORMnai>}
    BEKU_MO_NAI: {<す:.*><べく:.*><も:.*><A-NORMnai>}
    BEKU: {<V-cPRESp.*><べく:.*>}
    BEKU: {<す:.*><べく:.*>}

    BEKI_DEWA_NAI: {<す:.*><べき:.*><.*:DE><は:.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
    BEKI_DEWA_NAI: {<A-I><V-cPRESpARUx><べき:.*><.*:DE><は:.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
    BEKI_DEWA_NAI: {<A-NA><.*:DE><V-cPRESpARUx><べき:.*><.*:DE><は:.*><E-cPRESn|V-.*nARUx|A-NORMnai>}
    BEKI_DEWA_NAI: {<V-cPRESp.*><べき:.*><.*:DE><は:.*><E-cPRESn|V-.*nARUx|A-NORMnai>}

    BEKI_DA: {<す:.*><べき:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
    BEKI_DA: {<A-I><V-cPRESpARUx><べき:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
    BEKI_DA: {<A-NA><.*:DE><V-cPRESpARUx><べき:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
    BEKI_DA: {<V-cPRESp.*><べき:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}


    KEDO/KEREDO/KEREDOMO: {<けど:.*|けれど:.*|けれども:.*>}

    YORI~HOU~GA: {<NP.*><より:.*><.*>*<NP.*><の:.*><ほう:.*|NP-HOU><が:.*>}
    YORI~HOU~GA: {<V-c.*><より:.*><.*>*<V-c.*><ほう:.*|NP-HOU><が:.*>}

    HANMEN: {<V-cPRES.*|A-NORM.*|A-Idict><反面:.*>}
    HANMEN: {<A-NA><な:.*><反面:.*>}
    HANMEN: {<NP.*|A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<反面:.*>}

	HOU_GA_II: {<V-c.*><ほう:.*|NP-HOU><が:.*><A-NORMii>}	
	HOU_GA_II: {<YORI~HOU~GA><A-NORMii>}												# nested rule

	MAJIKI: {<V-cPRESp.*><まじき:.*>}


 	KAI_MO_NAKU: {<V-c.*><NP-KAI><も:.*><A-NORMnaku>}
  	KAI_MO_NAKU: {<NP.*><の:.*><NP-KAI><も:.*><A-NORMnaku>}
 	MO_TOUZEN_DA: {<V-c.*><NP-NO><も:.*><当然:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	MO_TOUZEN_DA: {<V-TEp.*><も:.*><当然:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
   	NO_MO_MOTTO_MO_DA: {<V-c.*><NP-NO><も:.*><は:.*>?<もっとも:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
  	NO_MO_MOTTO_MO_DA: {<NP.*><も:.*><もっとも:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    MOTTO_MO: {<もっとも:.*>}
    MO: {<NP.*><も:.*>}

    AGEKU: {<V-cPASTp><NP-AGEKU><に:.*>?}
    AGEKU: {<NP.*><の:.*><NP-AGEKU><に:.*>?}

  	AIDA_NI: {<V-cPRES.*><NP-AIDA><に:.*>}	
 	AIDA_NI: {<A-NA><な:.*><NP-AIDA><に:.*>}
 	AIDA_NI: {<A-Idict><NP-AIDA><に:.*>}
 	AIDA_NI: {<NP.*><の:.*><NP-AIDA><に:.*>}
  	AIDA: {<V-cPRESp.*><NP-AIDA>}	
 	AIDA: {<NP.*><の:.*><NP-AIDA>}

 	BA~HODO: {<V-cBA><V-cPRESp><ほど:.*>}
 	BA~HODO: {<A-NA><なら:.*><A-NA><な:.*><ほど:.*>}
 	BA~HODO: {<A-cBA><A-I><ほど:.*>}

 	BA~NONI: {<V-cBA><.*>*<のに:.*>}
 	BA~NONI: {<A-NA|NP.*><なら:.*><.*>*<の:.*|NP-NO><に:.*>}
 	BA~NONI: {<A-cBA><.*>*<のに:.*>}

	MOSHIMO~TARA: {<もしも:.*><.*>*<V-TARA>}


    TOKORO_O: {<V-c.*|A-NORM.*|A-Idict><NP-TOKORO><を:.*>}
    TOKORO_O: {<A-NA><な:.*><NP-TOKORO><を:.*>}
    TOKORO_O: {<NP.*><の:.*><NP-TOKORO><を:.*>}
    TA_TOKORO_DE: {<V-cPAST.*><NP-TOKORO><E-cTEp>}
    TA_TOKORO: {<V-cPAST.*><NP-TOKORO>}
    TOKORO_DATTA: {<V-cPRESp.*><NP-TOKORO><E-cPASTdattap>}
    TOKORO: {<V-cPRES.*><NP-TOKORO>}

    CHITTO_MO~NAI: {<ちっとも:.*><V-.*n>}

    BEKARAZU: {<V-cPRESp.*><べから:.*><ず:.*>}

    BAKARI_DENAKU: {<NP.*|V-c.*|A-NORM.*|A-Idict><ばかり:.*><.*:DE><E-cPRESn>}
    BAKARI_DENAKU: {<A-NA><な:.*><ばかり:.*><.*:DE><E-cPRESn>}
    BAKARI_KA: {<NP.*|V-c.*|A-NORM.*|A-Idict><ばかり:.*><か:.*>}
    BAKARI_KA: {<A-NA><な:.*><ばかり:.*><か:.*>}
    BAKARI_NI: {<V-c.*|A-NORM.*|A-Idict><ばかり:.*><に:.*>}
    BAKARI_NI: {<A-NA><な:.*><ばかり:.*><に:.*>}
    BAKARI_NI: {<NP.*|A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<ばかり:.*><に:.*>}
  	BAKARI_DA: {<V-cPRESp.*><ばかり:.*><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    BAKARI_DE: {<V-c.*|A-Idict><ばかり:.*><.*:DE|E-cTEp>}
    BAKARI_DE: {<V-c.*|A-Idict><ばかり:.*><.*:DE|E-cTEp>}
    BAKARI_DE: {<A-NA><な:.*><ばかり:.*><.*:DE|E-cTEp>}
    V-cTA_BAKARI: {<V-cPAST.*><ばかり:.*>}
    V-cBAKARI: {<V-TEp><ばかり:.*>}
    V-cBAKARI: {<NP.*><ばかり:.*>}

    TO_IU_FUU_NI: {<という:.*|TO_IU><NP-FUU><に:.*>}
    FUU_NI: {<NP-FUU><に:.*>}

    GOTO_NI: {<V-cPRESp.*><NP-GOTO><に:.*>}
    GOTO_NI: {<NP.*><NP-GOTO><に:.*>}

    HODO: {<NP.*|V-cPRES.*|A-NORM.*|A-Idict><程:.*|ほど:.*>}
    HODO: {<A-NA><な:.*><程:.*|ほど:.*>}


    IJOU_NI: {<V-c.*|NP.*|A-NA|A-Idict><NP-IJOU><に:.*>}
    IJOU_NI: {<NP-IJOU><の:.*><NP.*>}

    IJOU_WA: {<V-c.*|A-Idict><NP-IJOU><は:.*>?}
    IJOU_WA: {<NP.*|A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<NP-IJOU><は:.*>?}

    TE_DEMO: {<V-TEp><でも:.*>}
    TE_IRAI: {<V-TEp><NP-IRAI>}
    TE_KOSO: {<V-TEp><NP-KOSO|こそ:.*>}
    TEWA_NARANAI: {<V-TEp><は:.*><V-.*nNARU>}
    TE_NARANAI: {<V-TEp><V-.*nNARU>}
    TE_NARANAI: {<A-NA|A-I><E-cTEp><V-.*nNARU>}


    KARA_KOSO: {<V-c.*><から:.*><NP-KOSO>}
    KARA_KOSO: {<NP.*><E-cPASTp><から:.*><NP-KOSO>}


    KARA_NIWA: {<V-cPRESp|V-cPAST.*><からには:.*>}

    KAWARI_NI: {<V-c.*><NP-KAWARI><に:.*>}
    KAWARI_NI: {<NP.*><の:.*><NP-KAWARI><に:.*>}
    KAWARI_NI: {<その:.*><NP-KAWARI><に:.*>}

    KEKKA: {<V-cPAST.*><NP-KEKKA>}
    KEKKA: {<NP.*><の:.*><NP-KEKKA>}
    KEKKA: {<その:.*><NP-KEKKA>} 

    NAI_KOTO_WA_NAI: {<V-cPRESn.*|A-NORM.*><NP-KOTO><は:.*><E-.*n|V-.*nARUx|A-NORMnai>}
    NAI_KOTO_WA_NAI: {<NP.*|A-NA><じゃ:.*><E-cPRESn><NP-KOTO><は:.*><E-.*n|V-.*nARUx|A-NORMnai>}
    NAI_KOTO_WA_NAI: {<NP.*|A-NA><.*:DE><は><E-cPRESn><NP-KOTO><は:.*><E-.*n|V-.*nARUx|A-NORMnai>}

    KOTO_WA_NAI: {<V-cPRESp.*><NP-KOTO1pres><は:.*><E-.*n|V-.*nARUx|A-NORMnai>}

    KOTO_KARA: {<V-c.*|A-NORM.*|A-Idict><NP-KOTO><から:.*>}
    KOTO_KARA: {<NP.*|A-NA><E-cPASTdattap><NP-KOTO><から:.*>}
    KOTO_KARA: {<NP.*|A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<NP-KOTO><から:.*>}

    KOTO2: {<V-cPRES.*><NP-KOTO>}


    KUSE_NI: {<V-cPRESp|A-NORM.*|A-Idict><NP-KUSE><に:.*>}
    KUSE_NI: {<A-NA><な:.*><NP-KUSE><に:.*>}
    KUSE_NI: {<MP.*><の:.*><NP-KUSE><に:.*>}

    MARU_DE: {<まるで:.*><V-c.*><NP-YOU>}
    MARU_DE: {<まるで:.*><NP.*><の:.*><NP-YOU>}
 	YOU_DA: {<V-c.*><NP-YOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	YOU_DA: {<A-Idict|A-NORM.*><NP-YOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	YOU_DA: {<A-NA><な:.*><NP-YOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	YOU_DA: {<NP.*><の:.*><NP-YOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}

 	KA_NO_YOU_NI: {<V-c.*><か:.*><の:.*><NP-YOU><に:.*|な:.*|です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	KA_NO_YOU_NI: {<NP.*|A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<か:.*><の:.*><NP-YOU><に:.*>}


 	YOU_NI/YOU_NA: {<V-c.*><NP-YOU><に:.*|な:.*>}
 	YOU_NI/YOU_NA: {<NP.*><の:.*><NP-YOU><に:.*|な:.*>}

 	MONO_NARA: {<V-cRARERU|V-cPRES.*><NP-MONO|NP-MON><なら:.*>}

 	MONONO: {<V-c.*|A-NORM.*|A-Idict><ものの:.*>}
 	MONONO: {<A-NA><な:.*><ものの:.*>}
 	MONONO: {<NP.*>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<ものの:.*>}

 	NAKA_O/NAKA_DEWA: {<V-c.*|A-.*><NP-NAKA><を:.*>}
 	NAKA_O/NAKA_DEWA: {<NP.*><の:.*><NP-NAKA><を:.*>}
 	NAKA_O/NAKA_DEWA: {<V-c.*|A-.*><NP-NAKA><E-cTEp><は:.*>}
 	NAKA_O/NAKA_DEWA: {<NP.*><の:.*><NP-NAKA><E-cTEp><は:.*>}
    NO_NAKA_DE: {<NP.*><の:.*><NP-NAKA><E-cTEp>}

    NAKU_WA_NAI: {<V-cPRESn|A-NORM.*><は:.*|も:.*><E-.*n|V-.*nARUx|A-NORMnai>}
    NAKU_WA_NAI: {<NP.*><が:.*><A-NORMnaku><は:.*|も:.*><E-.*n|V-.*nARUx|A-NORMnai>}

    NAI_MADE_MO: {<V-cPRESn><まで:.*><も:.*>}
    NAI_MADE_MO: {<NP.*><.*:DE><E-cPRESn><まで:.*><も:.*>}


 	NI_ATATTE: {<V-cPRESp|NP.*><にあたって:.*|にあたり:.*><は:.*>?}
 	NI_ATATTE: {<V-cPRESp|NP.*><にあたり:.*>}
 	NI_CHIGAI_NAI: {<NP.*|V-cPRES.*|A-NORM.*|A-Idict|A-NA><に:.*><NP-CHIGAI><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	NI_SAISHITE: {<V-cPRESp|NP.*><に際して:.*><は:.*>?}
 	NI_TSUKE: {<V-cPRESp.*><につけ:.*>}
  	NI_TSUKE: {<NP.*><につけ:.*>}
 	NI_TSUKE: {<V-cPRESp.*><に:.*><つけ:.*>}
  	NI_TSUKE: {<NP.*><に:.*><つけ:.*>}

    IZURE_NISE_YO: {<NP-IZURE><に:.*><せよ:.*>}
  	NI_SEYO/NI_SHIRO: {<V-c.*|A-NORM.*|A-Idict><に:.*><せよ:.*|しろ:.*>}
  	NI_SEYO/NI_SHIRO: {<NP.*|A-NA>((<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>))?<に:.*><せよ:.*|しろ:.*>}

  	NI_SHIRO~NI_SHIRO: {<NI_SEYO/NI_SHIRO><.*>?<NI_SEYO/NI_SHIRO>}

  	NI_SOUI_NAI: {<V-c.*|A-NORM.*|A-Idict><に:.*><NP-SOUI><E-cPRESn|V-.*nARUx|A-NORMnai>}
  	NI_SOUI_NAI: {<NP.*|A-NA>((<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>))?<に:.*><NP-SOUI><E-cPRESn|V-.*nARUx|A-NORMnai>}

  	MONO_DE: {<V-c.*><NP-MONO><.*:DE>}



  	KATAWARA: {<V-cPRESp><NP-KATAWARA>}
  	KATAWARA: {<NP.*><の:.*><NP-KATAWARA>}


 	OKAGE_DE: {<V-c.*|A-NORM.*|A-Idict><NP-OKAGE><E-cTEp>}
 	OKAGE_DE: {<A-NA><な:.*><NP-OKAGE><E-cTEp>}
 	OKAGE_DE: {<NP.*><の:.*><NP-OKAGE><E-cTEp>}

 	SEI_KA: {<V-c.*|A-NORM.*|A-Idict><NP-SEI><か:.*>}
 	SEI_KA: {<A-NA><な:.*|E-cPASTdattap><NP-SEI><か:.*>}
 	SEI_KA: {<NP.*><の:.*><NP-SEI><か:.*>}
 	SEI_DE: {<V-c.*|A-NORM.*|A-Idict|A-NA><NP-SEI><.*:DE|に:.*>?}
 	SEI_DE: {<NP.*><の:.*><NP-SEI><.*:DE|に:.*>?}

    DEMO_NAN_DEMO_NAI: {<NP.*|A-NA>(<でも:.*>|<で:.*><も:.*>)<NP-NANI><でも:.*><V-.*nARUx>}
 	TEMO: {<V-TE.*><も:.*>}
 	TEMO: {<NP.*|A-NA><でも:.*>}
 	TEMO: {<NP.*|A-NA><で:.*><も:.*>}
 	TEMO: {<A-I><E-cTEp><も:.*>}
	DEMO: {<でも:.*><、:.*>}


 	DONNA_NI~TEMO: {<どんなに:.*><TEMO>}
 	IKURA~TEMO: {<いくら:.*><TEMO>}
 	TATOE~TEMO: {<たとえ:.*><.*>*<TEMO>}


    TOTEMO~NAI: {<とても:.*><V-.*n.*>}


    GOTOKI/GOTOKU: {<V-c.*><ごとき:.*|ごとく:.*>}
    GOTOKI/GOTOKU: {<N.*><の:.*><ごとき:.*|ごとく:.*>}

 	TOWA_KAGIRANAI: {<V-c.*|A-NORM.*|A-Idict><と:.*><は:.*><NP-KAGIRI><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	TOWA_KAGIRANAI: {<NP.*|A-NA><E-cPASTp><と:.*><は:.*><NP-KAGIRI><E-cPRESn|V-.*nARUx|A-NORMnai>}
 	KAGIRI_DA: {<A-NORM.*|A-Idict><NP-KAGIRI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	KAGIRI_DA: {<A-NA><な:.*><NP-KAGIRI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
 	KAGIRI: {<V-c.*><NP-KAGIRI>}
 	KAGIRI: {<NP.*>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<NP-KAGIRI>}


 	TO_DOUJI_NI: {<NP.*|V-cPRES.*><と:.*><同時に:.*>}
 	TO_DOUJI_NI: {<A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<と:.*><同時に:.*>}

 	TO_II/TARA_II: {<V-cPRES.*><と:.*><A-NORMii>}
 	TO_II/TARA_II: {<V-TARA><A-NORMii>}

 	TOORI_NI: {<V-c.*p><NP-TOORI><に:.*>}
 	TOORI_NI: {<NP.*><の:.*><NP-TOORI><に:.*>}
 	TOORI_NI: {<NP.*><NP-DOORI><に:.*>}

 	TOSHITEMO: {<V-c.*|A-NORM.*|A-Idict><として:.*><も:.*>}
 	TOSHITEMO: {<NP.*|A-NA><E-cPASTp><として:.*><も:.*>}
 	WA_BETSU_TOSHITE: {<V-c.*|A-NORM.*|A-Idict|A-NA><か:.*>(<どう:.*><か:.*>|<どうか:.*>)<は:.*><NP-BETSU><として:.*>}
 	WA_BETSU_TOSHITE: {<NP.*><は:.*><NP-BETSU><として:.*>}
 	MONO_TOSHITE: {<NP.*|A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<NP-MONO><として:.*>}
 	MONO_TOSHITE: {<V-c.*|A-NORM.*|A-Idict><NP-MONO><として:.*>}
 	TOSHITE~NAI: {<として:.*><V-.*n.*>}
    TOSHITE: {<NP.*><として:.*>}

    SAICHUU_NI: {<V-cTEIRU><NP-SAICHUU><に:.*|E-cPASTp>}
    SAICHUU_NI: {<NP.*><の:.*><NP-SAICHUU><に:.*|E-cPASTp>}

    TOCHUU_DE/TOCHUU_NI: {<V-c.*><NP-TOCHUU><E-cTEp|に:.*>}
    TOCHUU_DE/TOCHUU_NI: {<NP.*><の:.*><NP-TOCHUU><E-cTEp|に:.*>}


 	TOWAIE: {<V-c.*|A-NORM.*|A-Idict|A-NA|NP.*><と:.*><は:.*><いえ:.*>}
 	TOWA: {<V-c.*|A-NORM.*|A-Idict><と:.*><は:.*>}
 	TOWA: {<NP.*|A-NA><E-cPASTp><と:.*><は:.*>}

    TEMAE: {<V-c.*><NP-TEMAE>}
    TEMAE: {<NP.*><の:.*><NP-TEMAE>}

    TA_HYOUSHI_NI: {<V-cPAST.*><NP-HYOUSHI><に:.*>?}
    TA_SHUNKAN_NI: {<V-cPAST.*><NP-SHUNKAN><に:.*>?}

    TSUIDE_NI: {<V-cPRESp.*><NP-TSUIDE><に:.*>}
    TSUIDE_NI: {<V-cPAST.*><NP-TSUIDE><に:.*>}
    TSUIDE_NI: {<NP.*><の:.*><NP-TSUIDE><に:.*>}

    UE_DE: {<V-cPRESp.*><NP-UE><E-cTEp>}
    UE_DE: {<V-cPAST.*><NP-UE><E-cTEp>}
    UE_DE: {<NP.*><の:.*><NP-UE><E-cTEp>}

    UE_NI: {<V-c.*|A-NORM.*|A-Idict><NP-UE><に:.*>}
    UE_NI: {<A-NA><な.*><NP-UE><に:.*>}
    UE_NI: {<NP.*><の:.*><NP-UE><に:.*>}

    UE_WA: {<V-c.*><NP-UE><は:.*>}


    NI_TSURETE: {<V-cPRESp.*><につれて:.*>}
    NI_TSURETE: {<NP.*><につれて:.*>}


 	UCHI_NI: {<V-c.*|A-NORM.*|A-Idict><NP-UCHI><に:.*>}
 	UCHI_NI: {<A-NA><な:.*><NP-UCHI><に:.*>}
 	UCHI_NI: {<NP.*><の:.*><NP-UCHI><に:.*>}

 	NI_WA: {<V-cPRESp.*><に:.*><は:.*>}

 	SAI_NI: {<V-cPRESp.*><NP-SAI><に:.*><は:.*>?}
 	SAI_NI: {<V-cPRESp.*><NP-SAI><は:.*>}
 	SAI_NI: {<V-cPAST.*><NP-SAI><に:.*><は:.*>?}
 	SAI_NI: {<V-cPAST.*><NP-SAI><は:.*>}
 	SAI_NI: {<NP.*><の:.*><NP-SAI><に:.*><は:.*>?}
 	SAI_NI: {<NP.*><の:.*><NP-SAI><は:.*>}
 	SAI_NI: {<この:.*|その:.*|あの:.*><NP-SAI><に:.*><は:.*>?}
 	SAI_NI: {<この:.*|その:.*|あの:.*><NP-SAI><は:.*>}

 	SOBA_KARA: {<V-cPRESp.*|V-cTEIRU|V-cPASTp><NP-SOBA><から:.*>}

 	SUE_NI: {<V-cPASTp><NP-SUE><に:.*>}
 	SUE_NI: {<NP.*><の:.*><NP-SUE><に:.*>}

 	TOKA~TOKA: {<V-cPRESp.*><とか:.*><.*>*<V-cPRESp.*><とか:.*>}
 	TOKA~TOKA: {<NP.*><とか:.*><.*>*<NP.*><とか:.*>}

 	TOKA_(DE): {<V-c.*|A-NORM.*|A-Idict><とか:.*><.*:DE>?}
 	TOKA_(DE): {<NP.*|A-NA><E-cPASTp><とか:.*><.*:DE>?}
  	TOKA_(DE): {<V-c.*|A-NORM.*|A-Idict><と:.*><か:.*><.*:DE>?}
 	TOKA_(DE): {<NP.*|A-NA><E-cPASTp><と:.*><か:.*><.*:DE>?}

 	TOMO: {<V-cPRESn|A-I><とも:.*>}


 	WARI_NI: {<V-c.*|A-NORM.*|A-Idict|A-NA><NP-WARI><に:.*>}
 	WARI_NI: {<NP.*><の:.*><NP-WARI><に:.*>}

 	YORIMO: {<NP.*|V-c.*><より:.*><も:.*>}


##### SENTENCE end
 	TATTE: {<V-cPASTp><って:.*>}
 	TATTE: {<A-I><E-cTEp>}
 	TATTE: {<A-NA><だって:.*>}
 	TATTE: {<V-SHITATTE>}

	KA_DOU_KA: {<V-c.*><か:.*>(<どう:.*><か:.*>|<どうか:.*>)}
 	KA_DOU_KA: {<A-.*><か:.*>(<どう:.*><か:.*>|<どうか:.*>)}
  	KA_DOU_KA: {<NP.*><か:.*>(<どう:.*><か:.*>|<どうか:.*>)}

    KANA: {<.*:Vdict><か:.*><な:.*>}
    KANA: {<A-.*><か:.*><な:.*>}
    KANA: {<NP.*><か:.*><な:.*>}


    YOU_DEWA_NAI_KA: {<V-IKOU_KEI><.*:DE><は:.*><E-cPRESn|V-.*nARUx|A-NORMnai><か:.*>}
    YOU_GA_NAI: {<V-IKOU_KEI><が:.*>?<V-.*nARUx>}

    DEWA_NAI_KA: {<.*:DE><は:.*><E-cPRESn|V-.*nARUx|A-NORMnai><か:.*>}
    MASEN_KA: {<V-pPRESn.*|E-pPRESn><か:.*>}
    NAI_MONO_KA: {<V-cPRESn><NP-MONO>(<E-cPASTp><う:.*>)?<か:.*>}
    JANAI_KA: {<じゃ:.*><E-cPRESn|V-.*nARUx|A-NORMnai><か:.*>}

    KOTO_DAKARA: {<V-.*|A-I><NP-KOTO><E-cPASTp><から:.*|し:.*>}
    KOTO_DAKARA: {<A-NORM.*|A-I><NP-KOTO><E-cPASTp><から:.*|し:.*>}
    KOTO_DAKARA: {<A-NA><な:.*|である:.*><NP-KOTO><E-cPASTp><から:.*|し:.*>}
    KOTO_DAKARA: {<NP.*><である:.*><NP-KOTO><E-cPASTp><から:.*|し:.*>}
    KOTO_DAKARA: {<NP.*><の:.*><NP-KOTO><E-cPASTp><から:.*>}

	NO_DESHOU_KA: {<V-c.*><NP-N|NP-NO>?<でしょ:.*><う:.*><か:.*>}
	NO_DESHOU_KA: {<A-.*>?<NP-N|NP-NO>?<でしょ:.*><う:.*><か:.*>}
	NO_DESHOU_KA: {<NP.*><な:.*>?<NP-N|NP-NO>?<でしょ:.*><う:.*><か:.*>}

	DESHOU: {<V-cPRESp.*><NP-N|NP-NO>?<でしょ:.*><う:.*>}
	DESHOU: {<A-.*>?<NP-N|NP-NO>?<でしょ:.*><う:.*>}
	DESHOU: {<NP.*><な:.*>?<NP-N|NP-NO>?<でしょ:.*><う:.*>}

	KA_NANI_KA: {<NP.*><か:.*><NP-NANI><か:.*>}

	KA_INA_KA: {<V-c.*|A-NORM.*|A-Idict><か:.*><NP-INA><か:.*>}
	KA_INA_KA: {<NP.*|A-NA>((<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>))?<か:.*><NP-INA><か:.*>}

    TA_MONO_DA: {<V-cPAST.*|E-cPASTp><NP-MONO><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
  	MONO_DA: {<V-c.*|A-I|A-NA><NP-MONO|NP-MON><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
  	MONO_DA: {<V-c.*|A-I|A-NA><NP-MONO|NP-MON><じゃ:.*><E-cPRESn>}
  	MONO_KA: {<V-c.*|A-I><NP-MONO|NP-MON><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?<か:.*>}
  	MONO_KA: {<NP.*|A-NA><な:.*><NP-MONO|NP-MON><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?<か:.*>}
  	MONO/MON: {<V-c.*|A-NORM.*|A-Idict|>(<NP-N><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>)?<NP-MONO|NP-MON>}
  	MONO/MON: {<NP.*|A-NA><な:.*>(<NP-N><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>)?<NP-MONO|NP-MON>}

	KA: {<か:.*><？:.*|。:.*>}															# Question to catch ka at the end
    KA~KA: {<A-.*><か:.*>}
    KA~KA: {<V-.*><か:.*>}
    KA~KA: {<NP.*><か:.*>}

    KARA1: {<NP.*><から:.*>}
    KARA2: {<V-.*><から:.*>}
    KARA2: {<A-NORM.*|A-I><から:.*>}
    KARA2: {<A-NA><E-cPASTp><から:.*>}
    KARA2: {<NP.*><E-cPASTp><から:.*>}

 	NAKANAKA~NAI: {<なかなか:.*><V-.*n.*>}



	DAKE_DE_NAKU: {<A-NA><な:.*><だけ:.*><.*:DE><E-cPRESn>}
	DAKE_DE_NAKU: {<A-NA><.*:DE><V-cPRESpARUx><だけ:.*><.*:DE><E-cPRESn>}
	DAKE_DE_NAKU: {<NP.*>(<.*:DE><V-cPRESpARUx>)?<だけ:.*><.*:DE><E-cPRESn>}
	DAKE_DE_NAKU: {<V-cPRESp.*|A-NORM.*|A-Idict><だけ:.*><.*:DE><E-cPRESn>}

	DAKE_DE: {<V-c.*><だけ:.*><.*:DE>}

	DAKE_NI: {<V-c.*|NP.*|A-NORM.*|A-Idict><だけ:.*><に:.*>}
	DAKE_NI: {<A-NA><な:.*><だけ:.*><に:.*>}

	DAKE: {<V-cPRESp.*><だけ:.*>}
	DAKE: {<.*:A-NA><な:.*><だけ:.*>}
	DAKE: {<.*:A-NORM.*|A-I><だけ:.*>}

	IPPOU_DA: {<V-cPRESp.*><NP-IPPOU|一方:.*><E-cPASTp>}
	IPPOU_DE: {<V-c.*|A-Idict><NP-IPPOU|一方:.*><E-cTEp>}
	IPPOU_DE: {<NP.*|A-NA>(<E-cPASTp><V-cPRESpARUx>|<E-cPASTdattap>)<NP-IPPOU|一方:.*><E-cTEp>}

	SHIMATSU_DA: {<V-cPRESp.*><NP-SHIMATSU><E-cPASTp>}


 	NARA: {<A-.*|V-c.*><:.*>?<なら:.*>}
 	NARA: {<NP.*><なら:.*>}

	NADO: {<NP.*><など:.*>}


    NODE: {<V-.*|A-NORM.*|A-Idict><ので:.*>}
    NODE: {<NP.*|A-NA><な:.*><ので:.*>}

    TAME_NI: {<V-.*|A-NORM.*|A-Idict><NP-TAME><に:.*>}
    TAME_NI: {<A-NA><な:.*><NP-TAME><に:.*>}
    TAME_NI: {<NP.*><の:.*><NP-TAME><に:.*>}

    TADA~NOMI_DA: {<ただ.*><.*>*<NP.*|V-cPRES.*><のみ:.*><E-cPASTp>}


    DEWA_ARU_MAI_SHI: {<V-.*|NP.*><E-cTEp><は:.*><V-cPRESpARUx><まい:.*><し:PARTICLE>}
    DEWA_ARU_MAI_SHI: {<V-.*|NP.*><じゃ:.*><V-cPRESpARUx><まい:.*><し:PARTICLE>}

    DEWA_ARU_MAI_KA: {<V-.*|NP.*><.*:DE><は:.*><V-cPRESpARUx><まい:.*><か:.*>}

    DANO~DANO: {<V-.*|A-NORM.*|A-Idict|NP.*|A-NA><E-cPASTdattap>?<だの:.*><.*>*<V-.*|A-NORM.*|A-Idict|NP.*|A-NA><E-cPASTdattap>?<だの:.*>}
    DANO~DANO: {<V-.*|A-NORM.*|A-Idict|NP.*|A-NA><E-cPASTdattap>?<だの:.*><.*>*<V-.*|A-NORM.*|A-Idict|NP.*|A-NA><E-cPASTdattap>?<E-cPASTp><NP-NO>}

    NARI_NI/NARI_NO: {<V-.*|A-.*|NP.*><なり:.*><に:.*>}
    NARI_NI/NARI_NO: {<V-.*|A-.*|NP.*><なり:.*><の:.*><NP.*>}

    NAKUSHITE_WA: {<NP.*><NAKUSHITE><は:.*>?}

    SHI: {<V-c.*><し:PARTICLE>}
    SHI: {<NP.*|A-NA><E-cPASTp|E-cPASTdattap><し:PARTICLE>}
    SHI: {<A-NORM.*|A-I><し:PARTICLE>}


    SOU_DA1: {<V-c.*><NP-SOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    SOU_DA1: {<NP.*|A-NA><E-cPASTp><NP-SOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
    SOU_DA1: {<A-NORM.*|A-Idict><NP-SOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}

    SOU_DA2: {<A-NA><NP-SOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
    SOU_DA2: {<A-I><NP-SOU><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}


    TO_IE_DOMO: {<V-.*|A-.*|NP.*><と:.*><いえ:Vba><ども:.*>}

    TAGA_SAIGO: {<V-TARA><NP-SAIGO>}
    TAGA_SAIGO: {<V-cPAST.*><が:.*><NP-SAIGO>}

    TARA: {<V-TARA>}
    TARA: {<NP.*><E-cPASTp|E-cPASTdattap><たら:.*>}

    TARA_DOU: {<TARA><ど:.*><う:.*>}
    TARA_DOU: {<TARA><どう:.*>}



    TA_TOTAN: {<V-cPAST.*|E-cPASTp><NP-TOTAN>}

    TABI_NI: {<NP.*><の:.*><NP-TABI><に:.*>}
    TABI_NI: {<V-cPRESp.*><NP-TABI><に:.*>}

 	MITAI_NA: {<NP.*><NP-MITAI><な:.*><NP.*>}
 	MITAI_NA: {<V-c.*><NP-MITAI><な:.*><NP.*>}

 	MITAI_NI: {<V-c.*><NP-MITAI><に:.*><V-.*|A-.*>}
 	MITAI_NI: {<NP.*><NP-MITAI><に:.*><V-.*|A-.*>}

 	TAMESHI_GA_NAI: {<V-cPAST.*><NP-TAME><A-NORMshiganai>}

    MITAI_DA: {<A-NA><E-cPASTdattap>?<みたい:.*|NP-MITAI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}	
    MITAI_DA: {<A-NORM.*|A-I><みたい:.*|NP-MITAI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
    MITAI_DA: {<V-c.*><みたい:.*|NP-MITAI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}
    MITAI_DA: {<NP.*><E-cPASTdattap>?<みたい:.*|NP-MITAI><です:.*|E-cPASTp|E-cPASTdattap|でした:.*>?}

    TSUMORI_DATTA: {<V-cPASTp|V-cTEIRU><NP-TSUMORI><E-cPASTdattap|でした:.*>}
    TSUMORI_DATTA: {<NP.*><の:.*><NP-TSUMORI><E-cPASTdattap|でした:.*>}
    TSUMORI_DATTA: {<V-cPASTp|V-cTEIRU><NP-TSUMORI><な:.*><のに:.*>}
    TSUMORI_DATTA: {<NP.*><の:.*><NP-TSUMORI><な:.*><のに:.*>}
    TSUMORI_DE: {<V-cPASTp><NP-TSUMORI><E-cTEp>}
    TSUMORI_DE: {<NP.*><の:.*><NP-TSUMORI><E-cTEp>}
    TSUMORI: {<V-c.*><NP-TSUMORI><です:.*|E-cPASTp>?}
    TSUMORI: {<NP.*><の:.*><NP-TSUMORI><です:.*|E-cPASTp>?}
  	TSUMORI: {<A-NA><な:.*><NP-TSUMORI><です:.*|E-cPASTp>?}
 	TSUMORI: {<A-NORM.*|A-I><NP-TSUMORI><です:.*|E-cPASTp>?}
    NONI2: {<V-cPRESp.*><のに:.*>}
    NONI2: {<V-cPRESp.*><の:.*><に:.*>}
    NONI1: {<V-c.*|A-NORM.*|A-I><のに:.*>}
    NONI1: {<NP.*|A-NA><な:.*><のに:.*>}

    NA:	{<V-cPRESp.*><な:.*>}

	SORE_DEMO: {<それでも:.*>}
	SORE_NI: {<それ:.*|NP-SORE><に:.*>}

    NO_YARA/MONO_YARA/KOTO_YARA: {<V-.*|A-NORM.*|A-Idict><NP-NO|NP-MONO><やら:.*>}
    NO_YARA/MONO_YARA/KOTO_YARA: {<A-NA><な:.*><NP-NO|NP-MONO><やら:.*>}
    NO_YARA/MONO_YARA/KOTO_YARA: {<V-.*|A-Idict><KOTO-YARA>}
    NO_YARA/MONO_YARA/KOTO_YARA: {<A-NA><な:.*><KOTO-YARA>}
    NO_YARA~NO_YARA: {<NO_YARA/MONO_YARA/KOTO_YARA><.*>*<NO_YARA/MONO_YARA/KOTO_YARA>}

    IKANIMO: {<いかにも:.*>}
    KATSUTE: {<かつて:.*>}
    MOHAYA: {<もはや:.*>}
    SAMONAITO: {<さも:.*><V-cPRESnARUx|A-NORMnai><と:.*>}
    TOKORO_DE: {<ところで:.*>}
    TOKORO_GA: {<ところが:.*>}
    TORIWAKE: {<とりわけ:.*>}

    BURI_NI: {<BURI><に:.*>}

    YA_INA_YA: {<V-cPRESp><や:.*><NP-INA><や:.*>}
    YA_INA_YA: {<V-cPRESp><や:.*>}


    OMAKE_NI: {<NP-OMAKE><に:.*>}
    SEKKAKU: {<せっかく:.*>}

 	YOU_DEWA: {<NP-YOU><.*:DE><は:.*>}
	DE: {<NP.*><で:.*|E-cTEp>}
    NI/E: {<NP.*><に:.*|へ:.*>}
    NE: {<ね:PARTICLE>}
    NO: {<の:PARTICLE>}
    TO: {<と:PARTICLE>}
    YO: {<よ:PARTICLE>}
    KASHIRA: {<かしら:PARTICLE>}
    KAI:{<かい:PARTICLE>}
    NDATTE: {<V-c*|A-NORM.*|A-Idict><NP-N><です:.*><って:.*>}
    NDATTE: {<V-c.*|A-NORM.*|A-Idict><NP-N><だって:.*>}
    NDATTE: {<V-c.*|A-NORM.*|A-Idict><NP-N><E-cPASTp><って:.*>}
    NDATTE: {<A-NA><な:.*><NP-N><です:.*><って:.*>}
    NDATTE: {<A-NA><な:.*><NP-N><だって:.*>}
    NDATTE: {<A-NA><な:.*><NP-N><E-cPASTp><って:.*>}

	NDESU/NO_DESU: {<NP-N|NP-NO><です:.*|E-cPASTp>}
    JANAI: {<NP-N|NP-NO>?<じゃ:.*><E-cPRESn>}
    KKE: {<V-.*><っけ:.*>}
    KKE: {<NP.*|A-NORM.*|A-I><E-cPASTp|E-cPASTdattap><っけ:.*>}

    MASAKA: {<まさか:.*><.*>*<V.*n.*>}

    SATE: {<さて:.*>}
    CHINAMINI: {<ちなみに:.*>}

    BA_II: {<V-cBA><A-NORMii>}
    BA_YOKATTA: {<V-cBA><A-NORMyokatta><のに:.*>?}
    BA~NONI: {<V-cBA><.*>*<のに:.*|NONI2>}

    ARUIWA: {<あるいは:.*>}
    KARA_KOSO: {<だからこそ:.*>}
    TOMO_AROU:{<とも:.*><あ:.*><NP-ROU>}
	TOMO~TOMO: {<NP.*|V-c.*|A-.*>(<とも:.*>|(<と:.*><も:.*>))<NP.*|V-c.*|A-.*>(<とも:.*>|(<と:.*><も:.*>))}

 	TOMO: {<とも:.*>}
 	TTEBA: {<って:.*><NP-BA|ば:.*>}
 	TTEBA: {<だって:.*><NP-BA|ば:.*>}

	AMARI~NAI: {<NP-AMARI|あまり:.*><.*>*<V-.*n.*>}
	MOSHIKA_SHITARA: {<もしか:.*><.*>*<KAMO_SHIRENAI>}
	NOWA~DA: {<V-c.*|A-NORM.*|A-I><NP-NO><は:.*><.*>*<です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}
	NOWA~DA: {<NP.*|A-NA><な:.*><NP-NO><は:.*><.*>*<です:.*|E-cPASTp|E-cPASTdattap|でした:.*>}

	NAIDE: {<V-TEn><.*>*<V-.*>}

    ''')

chunkParser = nltk.RegexpParser(grammar)	# load the grammar	



def rule_ident(text):
	sentences = re.split(r'(?<=[\！\？\。\「\」\』\『])\s+', text)
	trees = []
	for sentence in sentences:
		tagged = tokenize(sentence)					# tokenize input (no sentence splitting)
		if tagged:
			#tree.pretty_print()
			trees.append(chunkParser.parse(tagged))
	return trees

def traverse_tree(tree, x, is_subtree=False):
	for subtree in tree:
		if type(subtree) == nltk.tree.Tree:
			if (subtree.label()[-1] == '_' or not any(labelStart in subtree.label() for labelStart in ['E-', 'NP', 'V-TEp', 'A-NORM', 'A-I', 'A-Idict', 'A-NA'])) and subtree.label()[-1] != 'x':
				x.append('START:' + subtree.label())
			traverse_tree(subtree, x, True)
			if (subtree.label()[-1] == '_' or not any(labelStart in subtree.label() for labelStart in ['E-', 'NP', 'V-TEp', 'A-NORM', 'A-I', 'A-Idict', 'A-NA'])) and subtree.label()[-1] != 'x':
				x.append('END:' + subtree.label())
		elif type(subtree) == tuple:
			x.append(subtree[0])
	return x


def get_rule_fromDF(label, jlpt):
	label = label.replace('V-pPRESn', '')
	label = label.replace('V-pPRESp', '')
	label = label.replace('V-pPASTp', '')
	label = label.replace('V-pPASTn', '')
	label = label.replace('V-p', '')

	label = label.replace('V-cPRESn', '')
	label = label.replace('V-cPRESp', '')
	label = label.replace('V-cPASTp', '')
	label = label.replace('V-cPASTn', '')
	label = label.replace('V-c', '')
	label = label.replace('V-', '')


	label = label.replace('A-c', '')
	label = label.replace('A-p', '')
	label = label.replace('A-Idict', '')

	label = label.lower()
	label = label.replace('_', ' ') 
	ruleInfo = df.loc[df['ROMAJI-RULE'] == label]
	if  ruleInfo.size == 0 or ruleInfo['JLPT'].values[0] not in jlpt:
		ruleInfo = None

	return ruleInfo

def to_html(x, level):
	htmlRules = ''
	htmlText = ''
	ruleStack = []
	ruleSet = set()
	ruleEnd = True

	# Generate Marked Text HTML
	for element in x:
		if 'START' in element:
			ruleSet.add(element)

			ruleInfo = get_rule_fromDF(element.split(':')[1], level)
			if ruleInfo is not None:
				jlpt = ruleInfo['JLPT'].values[0] 
				ruleENG = ruleInfo['ROMAJI-RULE'].values[0] 
				ruleJAP=  ruleInfo['JAP-RULE'].values[0] 
				definition = ruleInfo['DEFINITION'].values[0].replace('\n', ' <br />\n')
				
				ruleStack.append(ruleInfo)

		elif 'END' in element:
			ruleInfo = get_rule_fromDF(element.split(':')[1], level)
			if ruleInfo is not None:
				definition = '(' +ruleInfo['ROMAJI-RULE'].values[0] + ' ' + ruleInfo['JLPT'].values[0] +  ') ' + ruleInfo['DEFINITION'].values[0].replace('\n', ' <br />\n')
				htmlText = htmlText + '<div class="pop-up">\n' + definition + '</div></span>'
				ruleEnd = True

				if ruleStack:
					htmlText = htmlText + '<span class="pop-up-text" style="color:' + ruleStack[-1]['COLOR'].values[0] + '">'
					del ruleStack[-1]
					ruleEnd = False
		else:
				if ruleStack and ruleEnd:
					htmlText = htmlText + '<span class="pop-up-text" style="color:' + ruleStack[-1]['COLOR'].values[0] + '">' + element
					del ruleStack[-1]
					ruleEnd = False
				else:
					htmlText = htmlText + element
	# Generate Rule HTML
	for label in ruleSet:
		ruleInfo = get_rule_fromDF(label.split(':')[1], level)
		if ruleInfo is not None:
			jlpt = ruleInfo['JLPT'].values[0] 
			ruleENG = ruleInfo['ROMAJI-RULE'].values[0] 
			ruleJAP=  ruleInfo['JAP-RULE'].values[0] 
			definition = ruleInfo['DEFINITION'].values[0].replace('\n', ' <br />\n')
			htmlRules = htmlRules + '<li>'+ jlpt + '&nbsp;<span class="pop-up-text" value="' + ruleENG + '">' + ruleJAP + '<div class="pop-up">\n' +  definition + '\n</div></span></li>\n'

	return htmlRules, htmlText

'''
s = u'この質問には答えづらいです。'

trees = rule_ident(s)
marked = []
for tree in trees:
	print(tree)
	marked.extend(traverse_tree(tree, []))

print(to_html(marked,['N3','N1','N2','N4', 'N5'])[1])

print(marked)
'''


countYes = 0
countNo = 0
for index, row in df.iterrows():
	if isinstance(row['EXAMPLES'], str):
		examples = row['EXAMPLES'].split('\n')
		switch = False
		if len(examples) < 3:
			print('less than 3 examples: ',row['ROMAJI-RULE'])
		if len(examples) > 3:
			print('more than 3 examples: ',row['ROMAJI-RULE'])
		for sentence in examples:
			marked = []
			trees = rule_ident(sentence)
			for tree in trees:
				marked.extend(traverse_tree(tree, []))

				rule = 'START:' + row['ROMAJI-RULE'].replace(' ','_').upper()
				ruleAlt = 'START:V-c' + row['ROMAJI-RULE'].replace(' ','_').upper()
				ruleAlt3 = 'START:NP-' + row['ROMAJI-RULE'].replace(' ','_').upper() + '_'
				ruleAlt4 = 'START:V-p' + row['ROMAJI-RULE'].replace(' ','_').upper()
				ruleAl2 = 'START:A-Idict' + row['ROMAJI-RULE'].replace(' ','_').upper()

				if rule in marked or ruleAlt in marked or ruleAlt3 in marked or ruleAlt4 in marked:
					countYes = countYes + 1
					switch = True
				else:
					countNo = countNo + 1
					#print(row['ROMAJI-RULE'], tree)
		if switch == False:
			print('not found in any sentence: ',row['ROMAJI-RULE'])

print('yes: ', countYes, '   no: ', countNo)

