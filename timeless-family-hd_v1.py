# =====================================================================
# 👨‍👩‍👧 親子 Not-Self 条件付け分析ツール
# 両親のHDから、子供が幼少期に受けた条件付けを推測
# =====================================================================
 
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, date
import calendar
 
st.set_page_config(page_title="親子 Not-Self 分析", layout="wide", page_icon="👨‍👩‍👧")
 
# --- 🔐 パスワード認証 ---
def check_password():
    if "password_correct" not in st.session_state:
        st.session_state["password_correct"] = False
    if st.session_state["password_correct"]: 
        return True
    
    st.markdown("<h1 style='text-align: center; color: #00BFFF;'>👨‍👩‍👧 親子 Not-Self 分析</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>両親のHDから、子供が受けた条件付けを推測</p>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        pwd = st.text_input("Access Code", type="password")
        if st.button("System Login"):
            if pwd == "":
                st.session_state["password_correct"] = True
                st.rerun()
            else: 
                st.error("Access Denied.")
    return False
 
if not check_password(): 
    st.stop()
 
# --- センター名と色設定 ---
CENTER_NAMES = ['頭脳', '思考', '表現', '自己', '意志', '生命力', '直感', '感情', '活力']
CENTER_COLORS = {
    '頭脳': '#9C27B0', '思考': '#3F51B5', '表現': '#2196F3',
    '自己': '#4CAF50', '意志': '#FF9800', '生命力': '#F44336',
    '直感': '#795548', '感情': '#E91E63', '活力': '#FF5722'
}
 
# --- Not-Self 条件付けデータベース ---
NOTSELF_DATABASE = {
    '頭脳': {
        'open_theme': '他人の疑問を自分の疑問だと思い込む',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「確信を持って考える」タイプ',
                'message': [
                    '「ちゃんと考えなさい」',
                    '「答えを出しなさい」',
                    '「もっと深く考えろ」'
                ],
                'impact': '常に「答えを出さなければ」というプレッシャーを感じる。実際には答えが必要ない場面でも、無理に結論を出そうとして疲弊する。'
            },
            'one_defined': {
                'pattern': '片親が「確信」、片親が「疑問を拾う」タイプ',
                'message': [
                    '定義親：「自分で考えて決めなさい」',
                    '未定義親：「あれもこれも心配ね」'
                ],
                'impact': '確信を持つことと、あらゆる可能性を心配することの間で引き裂かれる。どちらが正しいのか分からず混乱。'
            },
            'both_open': {
                'pattern': '両親とも「疑問を拾う」タイプ',
                'message': [
                    '「世の中は複雑だ」',
                    '「簡単に答えは出ない」',
                    '「もっと調べなければ」'
                ],
                'impact': '家庭全体が「答えのない不安」で満ちている。子供も無意識に「考え続けなければ不安」というパターンを身につける。'
            }
        },
        'liberation': '「その疑問は、私が今考えることではない」と気づき、手放す。答えが必要な時だけ、インスピレーションを受け取る。'
    },
    
    '思考': {
        'open_theme': '他人の考え方を自分の考えだと思い込む',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「一貫した思考」を持つタイプ',
                'message': [
                    '「一度言ったことは守りなさい」',
                    '「コロコロ意見を変えるな」',
                    '「筋を通せ」'
                ],
                'impact': '柔軟に考えを変えることが「悪」だと刷り込まれる。新しい情報を取り入れられず、思考が硬直化。'
            },
            'one_defined': {
                'pattern': '片親が「一貫」、片親が「柔軟」',
                'message': [
                    '定義親：「ブレるな」',
                    '未定義親：「色んな考え方があるわね」'
                ],
                'impact': '一貫性を求められつつ、柔軟性も期待される矛盾。どちらにも応えられず自己否定。'
            },
            'both_open': {
                'pattern': '両親とも「柔軟すぎる」タイプ',
                'message': [
                    '「まあ、どっちでもいいんじゃない？」',
                    '「その時々で変わるよね」',
                    '親自身が一貫性がない'
                ],
                'impact': '「軸がない」家庭環境。子供は「自分の考え」を持つことの価値を学べず、常に周りに流される。'
            }
        },
        'liberation': '「昨日の私と今日の私は、成長した別の私」と許可する。新しい情報で常にアップデートできる柔軟性を取り戻す。'
    },
    
    '表現': {
        'open_theme': '沈黙を恐れ、思ってもないことを話す',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「自分から話す」タイプ',
                'message': [
                    '「ちゃんと説明しなさい」',
                    '「黙ってないで言いなさい」',
                    '「発言しないと存在しないのと同じ」'
                ],
                'impact': '聞かれていなくても話さなければ価値がないと思い込む。結果、空回りして「うるさい人」と思われる。'
            },
            'one_defined': {
                'pattern': '片親が「話す」、片親が「待つ」',
                'message': [
                    '定義親：「もっとはっきり言え」',
                    '未定義親：「静かにしてなさい」'
                ],
                'impact': '話すべきか黙るべきか、常に迷う。どちらを選んでも責められる感覚。'
            },
            'both_open': {
                'pattern': '両親とも「待つ」タイプ',
                'message': [
                    '「おとなしくしていなさい」',
                    '「余計なことは言わない」',
                    '家庭が静かすぎる'
                ],
                'impact': '自分の声を出すことへの罪悪感。本当に伝えたいことも、言い出せなくなる。'
            }
        },
        'liberation': '「聞かれるまで待つのが、私の自然な状態」と受け入れる。求められた時だけ、最も説得力のある言葉が出る。'
    },
    
    '自己': {
        'open_theme': '「本当の自分」を探し続けて迷走',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「確固たる自分」を持つタイプ',
                'message': [
                    '「自分らしさを大切に」',
                    '「ブレない自分でいなさい」',
                    '「芯を持て」'
                ],
                'impact': '環境で変わる自分を「ブレている」と否定。固定した自分を作ろうとして苦しむ。'
            },
            'one_defined': {
                'pattern': '片親が「固定」、片親が「流動」',
                'message': [
                    '定義親：「自分を持て」',
                    '未定義親：「周りに合わせなさい」'
                ],
                'impact': '矛盾するメッセージに混乱。「自分らしさ」と「適応」の間で引き裂かれる。'
            },
            'both_open': {
                'pattern': '両親とも「流動的」タイプ',
                'message': [
                    '「みんなに合わせていればいい」',
                    '「その場その場で変われ」',
                    '親自身が環境で変わる'
                ],
                'impact': '「自分らしさ」という概念自体を持てない。常に周りの期待に応えようとして疲弊。'
            }
        },
        'liberation': '「環境によって変わるのが、私の自然な状態」と受け入れる。カメレオンのように、どこでも適応できる強さを取り戻す。'
    },
    
    '意志': {
        'open_theme': '自分の価値を証明しようと無理な約束をする',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「意志が強い」タイプ',
                'message': [
                    '「やると言ったらやり遂げろ」',
                    '「約束は絶対守れ」',
                    '「弱音を吐くな」'
                ],
                'impact': '自分のキャパシティを無視して約束し、壊れるまで頑張る。休むことへの罪悪感。'
            },
            'one_defined': {
                'pattern': '片親が「強い意志」、片親が「柔軟」',
                'message': [
                    '定義親：「根性を見せろ」',
                    '未定義親：「無理しなくていいのよ」'
                ],
                'impact': '頑張るべきか休むべきか、常に迷う。どちらを選んでも罪悪感。'
            },
            'both_open': {
                'pattern': '両親とも「意志が弱い」タイプ',
                'message': [
                    '「約束は破れる」',
                    '「無理はしない」',
                    '親自身が約束を守らない'
                ],
                'impact': '「意志の強さ」への憧れと劣等感。過剰に証明しようとして、無理な約束を乱発。'
            }
        },
        'liberation': '「証明すべきことは何もない」と受け入れる。体が「無理」と言ったら、堂々と断る。'
    },
    
    '生命力': {
        'open_theme': '他人のペースに引きずられて疲弊',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「働き続ける」タイプ',
                'message': [
                    '「みんな働いている」',
                    '「休むのは怠け者」',
                    '「体が動くうちは働け」'
                ],
                'impact': '休息への罪悪感。体が悲鳴を上げても、親と同じペースで動こうとして壊れる。'
            },
            'one_defined': {
                'pattern': '片親が「働き続ける」、片親が「省エネ」',
                'message': [
                    '定義親：「もっと動け」',
                    '未定義親：「疲れたわ」'
                ],
                'impact': '「働く親が正しい」と思い込み、省エネ親を軽蔑。自分も無理して働き続ける。'
            },
            'both_open': {
                'pattern': '両親とも「省エネ」タイプ',
                'message': [
                    '「疲れやすい家族」',
                    '「無理はしない」',
                    '家庭全体がエネルギー不足'
                ],
                'impact': '「働き続ける人」への劣等感。社会に出て、周りのペースに合わせようとして壊れる。'
            }
        },
        'liberation': '「電池が切れる前に、自分から先に休む」と決める。他人のペースではなく、自分のリズムを信頼。'
    },
    
    '直感': {
        'open_theme': '古い恐怖に縛られ、合わない環境に居続ける',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「瞬時に察知」タイプ',
                'message': [
                    '「理由を説明しろ」',
                    '「根拠のない不安は無視しろ」',
                    '「論理的に考えろ」'
                ],
                'impact': '直感を否定され、「なんとなく嫌」という感覚を無視する癖がつく。結果、危険を察知できず傷つく。'
            },
            'one_defined': {
                'pattern': '片親が「直感」、片親が「過去の恐怖」',
                'message': [
                    '定義親：「すぐ逃げろ」',
                    '未定義親：「昔こんなことがあったから…」'
                ],
                'impact': '「今の直感」と「過去の恐怖」を区別できず、不必要な恐怖に縛られる。'
            },
            'both_open': {
                'pattern': '両親とも「過去の恐怖」タイプ',
                'message': [
                    '「昔こうだったから、きっと今回も…」',
                    '「怖いことばかり起きる」',
                    '家庭全体が恐怖で満ちている'
                ],
                'impact': '家族全体の恐怖を背負い込み、常に不安。本当の危険と妄想を区別できない。'
            }
        },
        'liberation': '「なんとなく嫌」は絶対正しいと信頼。理由は後でいい。今の直感に従って、すぐ距離を置く。'
    },
    
    '感情': {
        'open_theme': '他人の感情の波に飲み込まれて即断即決し、後悔',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「感情の波」を持つタイプ',
                'message': [
                    '「今決めなさい」（親の波が高い時）',
                    '「やっぱりダメ」（親の波が低い時）',
                    '感情的な家庭'
                ],
                'impact': '親の感情の波を自分のものだと思い込み、その波で決断。後で「なんであの時…」と後悔の連続。'
            },
            'one_defined': {
                'pattern': '片親が「波あり」、片親が「冷静」',
                'message': [
                    '定義親：「今すぐ決めろ」（波の時）',
                    '未定義親：「落ち着いて考えなさい」'
                ],
                'impact': '「すぐ決める」と「待つ」の間で混乱。どちらが正しいのか分からず、決断を恐れる。'
            },
            'both_open': {
                'pattern': '両親とも「冷静」タイプ',
                'message': [
                    '「感情的になるな」',
                    '「冷静に判断しろ」',
                    '家庭に感情がない'
                ],
                'impact': '感情を抑圧。しかし外の世界で他人の感情を受け取り、それで決断して大失敗。'
            }
        },
        'liberation': '「この感情の波は、誰かのもの」と観察。一晩寝かせてから、クリアな状態で決断。'
    },
    
    '活力': {
        'open_theme': '外からのプレッシャーで焦り、ミス連発',
        'parent_conditioning': {
            'both_defined': {
                'pattern': '両親とも「常にプレッシャー」タイプ',
                'message': [
                    '「早くしなさい！」',
                    '「ぐずぐずするな！」',
                    '「今すぐやれ！」'
                ],
                'impact': '常に急かされる家庭。自分のペースを持つことを許されず、焦りが当たり前の状態に。'
            },
            'one_defined': {
                'pattern': '片親が「急かす」、片親が「マイペース」',
                'message': [
                    '定義親：「さっさとやれ」',
                    '未定義親：「急がなくても…」'
                ],
                'impact': '急ぐべきか待つべきか、常に混乱。どちらに合わせても怒られる感覚。'
            },
            'both_open': {
                'pattern': '両親とも「マイペース」タイプ',
                'message': [
                    '「ゆっくりでいいわよ」',
                    '「焦らなくていい」',
                    '家庭全体がのんびり'
                ],
                'impact': '社会に出て、周りの「焦り」に圧倒される。それを自分のものだと思い込み、パニックになる。'
            }
        },
        'liberation': '「人は人、私は私」と境界線を引く。他人の焦りは受け取らず、自分のペースを守る。'
    }
}
 
# --- データ読み込み ---
@st.cache_data
def load_hd_data(birth_date):
    """
    ユーザーが選択した生年月日に基づいて、4つのParquetファイルから最適な1つを読み込むわ！
    """
    if birth_date is None:
        return None

    year = birth_date.year

    # 14番ゲート特製：4分割の条件分岐
    if year < 1935:
        file_name = "HD_Archive_1.parquet"
    elif year < 1970:
        file_name = "HD_Archive_2.parquet"
    elif year < 2005:
        file_name = "HD_Archive_3.parquet"
    else:
        file_name = "HD_Archive_4.parquet"

    try:
        # ぱーけ（Parquet）を読み込み
        df = pd.read_parquet(file_name)
    except FileNotFoundError:
        st.error(f"⚠️ ファイル {file_name} が見つからないわ。GitHubにアップロードされているか確認して！")
        return None
    except Exception as e:
        st.error(f"⚠️ 読み込みエラーが発生したわ：{e}")
        return None

    if df.empty:
        return None

    # 日時処理：CSV由来の列名（UTC_Time または JST_Time）を活用 
    # Parquetは型を保持しているはずだけど、念のため変換しておくわね
    if 'UTC_Time' in df.columns:
        df['Datetime'] = pd.to_datetime(df['UTC_Time'])
    elif 'JST_Time' in df.columns:
        df['Datetime'] = pd.to_datetime(df['JST_Time'])
    
    df['Date'] = df['Datetime'].dt.date
    
    return df

# --- アプリのメイン処理内での使い方イメージ ---
# user_date = st.date_input("生年月日を入力してね")
# if user_date:
#     df = load_hd_data(user_date)
 
# --- UI開始 ---
st.title("👨‍👩‍👧 親子 Not-Self 条件付け分析")
st.markdown("**両親のヒューマンデザインから、あなたが幼少期に受けた条件付けを推測します**")
 
st.divider()
 
# --- 日付入力セクション ---
st.header("📅 生年月日の入力")
 
col1, col2, col3 = st.columns(3)
 
# 父親
with col1:
    st.subheader("👨 父親")
    father_year = st.selectbox("父 - 年", list(range(1900, 2044)), index=50, key="f_year")
    father_month = st.selectbox("父 - 月", list(range(1, 13)), key="f_month")
    max_day_f = calendar.monthrange(father_year, father_month)[1]
    father_day = st.selectbox("父 - 日", list(range(1, max_day_f + 1)), key="f_day")
    father_time_unknown = st.checkbox("時刻不明", value=True, key="f_time_unknown")
 
# 母親
with col2:
    st.subheader("👩 母親")
    mother_year = st.selectbox("母 - 年", list(range(1900, 2044)), index=52, key="m_year")
    mother_month = st.selectbox("母 - 月", list(range(1, 13)), key="m_month")
    max_day_m = calendar.monthrange(mother_year, mother_month)[1]
    mother_day = st.selectbox("母 - 日", list(range(1, max_day_m + 1)), key="m_day")
    mother_time_unknown = st.checkbox("時刻不明", value=True, key="m_time_unknown")
 
# 本人
with col3:
    st.subheader("👤 本人")
    child_year = st.selectbox("本人 - 年", list(range(1900, 2044)), index=75, key="c_year")
    child_month = st.selectbox("本人 - 月", list(range(1, 13)), key="c_month")
    max_day_c = calendar.monthrange(child_year, child_month)[1]
    child_day = st.selectbox("本人 - 日", list(range(1, max_day_c + 1)), key="c_day")
    child_time_unknown = st.checkbox("時刻不明", value=False, key="c_time_unknown")
    
    if not child_time_unknown:
        child_hour = st.selectbox("本人 - 時", list(range(24)), index=12, key="c_hour")
        child_minute = st.selectbox("本人 - 分", list(range(60)), index=0, key="c_minute")
 
if st.button("🔍 Not-Self 条件付けを分析", type="primary", use_container_width=True):
    st.session_state['analysis_done'] = True
 
if not st.session_state.get('analysis_done', False):
    st.info("👆 生年月日を入力して「分析」ボタンを押してください")
    st.stop()
 
st.divider()
 
# --- サンプルデータ生成（実データがない場合） ---
import random
 
def generate_sample_centers():
    """サンプルのセンター定義を生成"""
    centers = {}
    for center in CENTER_NAMES:
        centers[center] = random.choice([True, False])
    return centers
 
# サンプルで分析実行
father_centers = generate_sample_centers()
mother_centers = generate_sample_centers()
child_centers = generate_sample_centers()
 
# --- 分析結果表示 ---
st.header("📊 分析結果")
 
# 1. センター比較表
st.subheader("1️⃣ 家族のセンター定義状態")
 
comparison_data = []
for center in CENTER_NAMES:
    comparison_data.append({
        'センター': center,
        '父': '●' if father_centers[center] else '○',
        '母': '●' if mother_centers[center] else '○',
        '本人': '●' if child_centers[center] else '○',
        '父（定義）': father_centers[center],
        '母（定義）': mother_centers[center],
        '本人（定義）': child_centers[center]
    })
 
comparison_df = pd.DataFrame(comparison_data)
 
# スタイル適用
def style_centers(row):
    styles = [''] * len(row)
    
    # 父
    if row['父（定義）']:
        styles[1] = 'background-color: #4CAF50; color: white; font-weight: bold;'
    else:
        styles[1] = 'background-color: #FFEB3B; color: #333; font-weight: bold;'
    
    # 母
    if row['母（定義）']:
        styles[2] = 'background-color: #4CAF50; color: white; font-weight: bold;'
    else:
        styles[2] = 'background-color: #FFEB3B; color: #333; font-weight: bold;'
    
    # 本人
    if row['本人（定義）']:
        styles[3] = 'background-color: #4CAF50; color: white; font-weight: bold;'
    else:
        styles[3] = 'background-color: #FFEB3B; color: #333; font-weight: bold;'
    
    return styles
 
display_df = comparison_df[['センター', '父', '母', '本人']].copy()
styled_df = display_df.style.apply(style_centers, axis=1)
 
st.dataframe(styled_df, hide_index=True, use_container_width=True)
st.caption("● = 定義（色つき）　○ = 未定義（白）")
 
st.divider()
 
# 2. 両親の関係性分析
st.subheader("2️⃣ 両親の関係性が創る「家庭の空気」")
 
# 両親の未定義センターを抽出
father_open = [c for c in CENTER_NAMES if not father_centers[c]]
mother_open = [c for c in CENTER_NAMES if not mother_centers[c]]
both_open = list(set(father_open) & set(mother_open))
 
if both_open:
    st.warning(f"**⚠️ 両親とも未定義のセンター**: {', '.join(both_open)}")
    st.markdown("""
    両親ともに未定義のセンターは、**家庭全体がそのテーマで不安定**になります。
    - 子供は「これが普通」だと思い込み、同じパターンを無意識に繰り返します
    - 家庭に「答え」がないため、外の世界で過剰に補償しようとします
    """)
else:
    st.success("✅ 両親に共通の未定義センターはありません")
 
# 両親が補完し合っているセンター
father_defined_mother_open = [c for c in CENTER_NAMES if father_centers[c] and not mother_centers[c]]
mother_defined_father_open = [c for c in CENTER_NAMES if mother_centers[c] and not father_centers[c]]
 
if father_defined_mother_open or mother_defined_father_open:
    st.info("**💡 両親が補完し合っているセンター**")
    if father_defined_mother_open:
        st.markdown(f"- 父が定義、母が未定義: **{', '.join(father_defined_mother_open)}**")
    if mother_defined_father_open:
        st.markdown(f"- 母が定義、父が未定義: **{', '.join(mother_defined_father_open)}**")
    st.markdown("→ 互いの強みと弱みが噛み合い、バランスの取れた家庭になりやすい")
 
st.divider()
 
# 3. 本人への影響推論
st.subheader("3️⃣ あなたが受けた Not-Self 条件付けの推測")
 
child_open = [c for c in CENTER_NAMES if not child_centers[c]]
 
if not child_open:
    st.success("""
    ✨ **全センター定義**
    
    あなたは全てのセンターが定義されています。これは非常に稀なパターンです。
    
    **予測される幼少期**：
    - 両親や社会からの条件付けを、**自分のペースで取り入れる**ことができた
    - 他人の影響を受けにくく、**自分の内側で完結**していた
    - ただし、未定義センターを持つ人（大多数）の気持ちを理解しにくい面も
    
    **注意点**：
    - 「みんなもできるはず」と思い込み、他人に厳しくなりやすい
    - 未定義センターの人の「揺らぎ」を「弱さ」だと誤解しやすい
    """)
else:
    st.warning(f"**⚠️ あなたの未定義センター**: {', '.join(child_open)}")
    
    for center in child_open:
        with st.expander(f"📍 {center}センター - Not-Self 条件付けの詳細", expanded=True):
            data = NOTSELF_DATABASE[center]
            
            # 両親のパターンを判定
            father_def = father_centers[center]
            mother_def = mother_centers[center]
            
            if father_def and mother_def:
                pattern_key = 'both_defined'
            elif not father_def and not mother_def:
                pattern_key = 'both_open'
            else:
                pattern_key = 'one_defined'
            
            conditioning = data['parent_conditioning'][pattern_key]
            
            # 基本テーマ
            st.markdown(f"**🎭 未定義センターの基本テーマ**")
            st.info(data['open_theme'])
            
            # 両親のパターン
            st.markdown(f"**👨‍👩 両親のパターン**")
            st.write(conditioning['pattern'])
            
            # 受けたメッセージ
            st.markdown(f"**💬 幼少期に受けたメッセージ**")
            for msg in conditioning['message']:
                st.markdown(f"- {msg}")
            
            # 影響
            st.markdown(f"**⚠️ あなたへの影響（推測）**")
            st.error(conditioning['impact'])
            
            # 解放
            st.markdown(f"**✨ Not-Self からの解放**")
            st.success(data['liberation'])
 
st.divider()
 
# 4. ビジュアル：家族のセンター図
st.subheader("4️⃣ 家族のセンター定義マップ")
 
fig = go.Figure()
 
# 各家族メンバーのセンター状態を可視化
for i, (name, centers_dict) in enumerate([('父', father_centers), ('母', mother_centers), ('本人', child_centers)]):
    values = []
    colors = []
    
    for center in CENTER_NAMES:
        if centers_dict[center]:
            values.append(1)
            colors.append(CENTER_COLORS[center])
        else:
            values.append(0.3)
            colors.append('#EEEEEE')
    
    fig.add_trace(go.Bar(
        name=name,
        x=CENTER_NAMES,
        y=values,
        marker=dict(
            color=colors,
            line=dict(color='#333', width=1)
        ),
        text=[center if centers_dict[center] else '' for center in CENTER_NAMES],
        textposition='inside',
        hovertemplate='%{x}: %{text}<extra></extra>'
    ))
 
fig.update_layout(
    barmode='group',
    height=400,
    xaxis=dict(title='センター'),
    yaxis=dict(title='', showticklabels=False),
    legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
)
 
st.plotly_chart(fig, use_container_width=True)
 
st.divider()
 
# 5. アクションプラン
st.subheader("5️⃣ Not-Self を手放すアクションプラン")
 
if child_open:
    st.markdown("""
    ### 📝 実践ステップ
    
    **STEP 1：気づく（1週間）**
    - 日常で、未定義センターのテーマが出てくる瞬間を観察
    - 「あ、今これは○○センターの Not-Self だ」と気づく練習
    
    **STEP 2：観察する（2週間目）**
    - 両親から受け取ったメッセージを思い出す
    - 「これは私の声ではなく、親の声だ」と分離
    
    **STEP 3：手放す（3週間目〜）**
    - 解放の言葉を声に出して言う
    - 「その疑問は、私が今考えることではない」
    - 「昨日の私と今日の私は、成長した別の私」
    
    **STEP 4：新しいパターンを育てる（継続）**
    - 未定義センターの「本来の強み」を信頼
    - アンテナとして、情報を受け取るだけで終わらせる
    """)
else:
    st.markdown("""
    ### 📝 全センター定義の方へ
    
    **他者理解のステップ**
    
    **STEP 1：違いを認識する**
    - 大多数の人は、あなたと違い「未定義センター」を持っている
    - その人たちは、あなたが「当たり前」にできることができない
    
    **STEP 2：期待を手放す**
    - 「みんなもできるはず」という期待を手放す
    - 相手の設計図を尊重する
    
    **STEP 3：補完関係を楽しむ**
    - あなたの「完結性」と、相手の「柔軟性」が補い合う
    - お互いの強みを活かす関係を築く
    """)
 
st.divider()
 
# 6. ダウンロード
st.subheader("📥 分析レポートのダウンロード")
 
report_text = f"""
# 親子 Not-Self 条件付け分析レポート
 
## 基本情報
- 父親: {father_year}年{father_month}月{father_day}日
- 母親: {mother_year}年{mother_month}月{mother_day}日
- 本人: {child_year}年{child_month}月{child_day}日
 
## センター定義状態
 
### 父親
"""
 
for center in CENTER_NAMES:
    status = '定義' if father_centers[center] else '未定義'
    report_text += f"- {center}: {status}\n"
 
report_text += "\n### 母親\n"
for center in CENTER_NAMES:
    status = '定義' if mother_centers[center] else '未定義'
    report_text += f"- {center}: {status}\n"
 
report_text += "\n### 本人\n"
for center in CENTER_NAMES:
    status = '定義' if child_centers[center] else '未定義'
    report_text += f"- {center}: {status}\n"
 
report_text += f"""
 
## Not-Self 条件付けの推測
 
### 未定義センター: {', '.join(child_open) if child_open else 'なし（全センター定義）'}
"""
 
if child_open:
    for center in child_open:
        data = NOTSELF_DATABASE[center]
        father_def = father_centers[center]
        mother_def = mother_centers[center]
        
        if father_def and mother_def:
            pattern_key = 'both_defined'
        elif not father_def and not mother_def:
            pattern_key = 'both_open'
        else:
            pattern_key = 'one_defined'
        
        conditioning = data['parent_conditioning'][pattern_key]
        
        report_text += f"""
### {center}センター
 
**基本テーマ**: {data['open_theme']}
 
**両親のパターン**: {conditioning['pattern']}
 
**受けたメッセージ**:
"""
        for msg in conditioning['message']:
            report_text += f"- {msg}\n"
        
        report_text += f"""
**影響**: {conditioning['impact']}
 
**解放**: {data['liberation']}
 
---
"""
 
st.download_button(
    label="📄 レポートをダウンロード (TXT)",
    data=report_text.encode('utf-8'),
    file_name=f"NotSelf_Analysis_{child_year}{child_month:02d}{child_day:02d}.txt",
    mime='text/plain'
)
 
st.markdown("---")
st.caption("💡 このツールは推測に基づいています。実際の個別リーディングをご希望の場合は、認定リーダーにご相談ください。")
