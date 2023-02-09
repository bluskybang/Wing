"""Welcome to Pynecone! This file outlines the steps to create a basic app."""
from pcconfig import config
import pynecone as pc
import re

docs_url = "https://pynecone.io/docs/getting-started/introduction"
filename = f"{config.app_name}/{config.app_name}.py"

main_blue = 'rgba(50,130,245,1)'
main_dark_blue = 'rgba(0,180,255,0.9)'


class PhoneNumber(pc.Model, table=True):
    phonenumber: str


class users(pc.Model, table=True):
    user: str
    pwd: str
    name: str
    contact_dial: str
    verify: str


class State(pc.State):
    count = 0
    NumberInput = ''
    NumberList = []
    NumberZip = []
    loding = True
    InitialData = ''
    charge_price = 10000

    def alert(self, text):
        print()

    def increment(self):
        self.count += 1

    def decrement(self):
        self.count -= 1

    def NumberListGet(self, text):
        new_str = re.sub(r"[^0-9\,\-\n\s]", "", str(text))
        self.NumberInput = new_str
        if len(self.NumberInput) <= 13:
            if ' ' in text:
                if text == ' ':
                    self.NumberInput = ''
                else:
                    self.NumberZip.append(text[0:len(text)-1])
                    self.NumberInput = ''
                self.NumberZip = list(set(self.NumberZip))
            if ',' in text:
                if text == ',':
                    self.NumberInput = ''
                else:
                    self.NumberZip.append(text[0:len(text)-1])
                    self.NumberInput = ''
                self.NumberZip = list(set(self.NumberZip))
            if '\n' in text:
                if text == '\n':
                    self.NumberInput = ''
                else:
                    self.NumberZip.append(text[0:len(text)-1])
                    self.NumberInput = ''
                self.NumberZip = list(set(self.NumberZip))
        else:
            if ',' in text:
                for x in self.NumberInput.split(','):
                    self.NumberZip.append(x)
                self.NumberInput = ''
                self.NumberZip = list(set(self.NumberZip))

    def addNum(self):
        self.NumberInput += '\n'
        if self.NumberInput == '\n':
            self.NumberInput = ''
        else:
            self.NumberZip.append(self.NumberInput[0:len(self.NumberInput)-1])
            self.NumberInput = ''
            self.NumberZip = list(set(self.NumberZip))

    numberrr: str

    def add_phonenumber(self):
        with pc.session() as session:
            session.add(
                PhoneNumber(
                    phonenumber='fffff'
                )
            )
            session.commit()

    def get_phonenumber(self):
        with pc.session() as session:
            self.numberrr = (
                session.query(PhoneNumber)
                .filter(PhoneNumber.phonenumber.contains('fffff'))
                .all()
            )
            print(self.numberrr)

    def killnum(self, index):
        del self.NumberZip[index]
        self.NumberZip = self.NumberZip

    async def wait(self):
        self.loding = not self.loding

    def charge_4x0(self, text):
        if len(str(self.charge_price)) > len(text):
            self.charge_price = 0
        else:
            if len(text) >= 5:
                self.charge_price = int(
                    text[0:int(len(text))-1])*10+(int(text[-1:])*10000)
            else:
                self.charge_price = int(text)*10000


class ModalState(State):
    Excel_show = False

    def excel_modal_show(self):
        self.Excel_show = not self.Excel_show


class RegState(State):
    State = False

    def Sign_in(self):
        self.State = not self.State


class SignState(State):
    State = True

    def Sign_in(self):
        self.State = not self.State


def listofnumber(text, index):
    return pc.tr(
        pc.th(pc.text(index+' : '+text, minHeight='2vh',
              height='2vh', resize='none', width='100%', paddingLeft='1vw'), padding='1vw', width='70%'),
        pc.th(pc.image(src="/img/del.png", objectFit='contain', verticalAlign='top', minHeight='3vh', height='3vh',
              on_click=lambda x: State.killnum(index), width='100%', padding='0'),  paddingLeft='3vw', width='30%', padding='1vw'))


def loading():

    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_body(
                    pc.center(
                        pc.vstack(
                            pc.box(height='45vh'),
                            pc.circular_progress(
                                pc.circular_progress_label('Click!'), on_click=State.wait, is_indeterminate=True),
                        )
                    )
                )
            )
        ), size='full', is_centered=True, is_open=State.loding
    )


def register():
    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_header(
                    pc.vstack(
                        sms_logo(size=.7, photo=1.4),
                    )
                ),
                pc.modal_body(
                    pc.vstack(
                        pc.form_control(
                            pc.form_label("아이디", html_for="user_id"),
                            pc.input(),
                            is_required=True,
                        ),

                        pc.form_control(
                            pc.form_label("비밀번호", html_for="user_pw"),
                            pc.input(type_='number'),
                            is_required=True,
                        ),
                        pc.form_control(
                            pc.form_label("비밀번호 확인", html_for="user_pw_check"),
                            pc.input(type_='number'),
                            is_required=True,
                        ),
                        pc.form_control(
                            pc.form_label("성명", html_for="user_name"),
                            pc.input(
                                placeholder='&#xd64d;&#xae38;&#xb3d9;'),

                            is_required=True,
                        ),

                        pc.form_control(
                            pc.form_label("가입자 전화번호", html_for="phone_number"),
                            pc.hstack(pc.input(), pc.button('인증', color='white',  backgroundColor=main_blue,
                                                            width='20%'), width='100%'),
                            is_required=True,
                        ),



                        padding='1vw'),

                ),
                pc.modal_footer(
                    pc.button(
                        "회원가입", color='white',  margin='3px', backgroundColor=main_blue,
                    ),
                    pc.button(
                        "취소", margin='3px', on_click=RegState.Sign_in
                    ),
                ),
            ), backgroundColor='rgba(0, 0, 0, .4)', backdropFilter='blur(15px)'
        ),
        is_open=RegState.State
    )


def login():
    return pc.modal(
        pc.modal_overlay(
            register(),
            pc.modal_content(
                pc.modal_header(
                    pc.vstack(
                        sms_logo(size=.7, photo=1.4),
                    )
                ),
                pc.modal_body(
                    pc.vstack(pc.text('아이디', fontWeight='bold', width='100%'),
                              pc.input(), padding='1vw'),
                    pc.vstack(pc.text('비밀번호', fontWeight='bold', width='100%'),
                              pc.input(), padding='1vw'),

                ),
                pc.modal_footer(
                    pc.button(
                        "로그인", color='white', margin='3px', backgroundColor=main_blue, on_click=SignState.Sign_in
                    ),
                    pc.button(
                        "회원가입", margin='3px', on_click=RegState.Sign_in
                    ),
                ),
            ), backgroundColor='rgba(0, 0, 0, .4)', backdropFilter='blur(15px)'
        ),
        is_open=SignState.State,

    )


def excel_modal():
    return pc.modal(
        pc.modal_overlay(
            pc.modal_content(
                pc.modal_header("How to import Excel"),
                pc.modal_body(
                    Readexcel(),
                    pc.box(height='2vh'),
                    pc.text_area(value=State.NumberInput, placeholder="Please choose your contact list", overflow='hidden', fontSize='2vh', resize='none', height='3vh',
                                 on_focus=State.NumberListGet, width='100%', id='numberinput-excel')
                ),
                pc.modal_footer(
                    pc.button(
                        "Close", id='closebtn', marggitin='3px', on_click=ModalState.excel_modal_show
                    )
                ),
            ),
        ),
        is_open=ModalState.Excel_show,
    )


def index():
    return pc.center(
        pc.vstack(
            pc.center(
                pc.vstack(
                    sms_logo(),
                    pc.box(
                        pc.box(
                            pc.html(
                                '<video playsinline="" autoplay="autoplay" muted="muted" loop="loop" style="width: 100vw"><source src="/video/vod_index.mp4" type="video/mp4"></video>'),
                            width='100%', overflow='hidden', height='40vw'),
                        pc.box(pc.text('\"FAST SMS\"는', height='3vw', font_size='3vw', fontWeight='bolder', lineHeight='normal'),
                               pc.text('가장 안전한', font_size='9vw', height='10vw',
                                       fontWeight='bold', lineHeight='normal'),
                               pc.text('국제 문자 서비스 입니다.', font_size='3vw', height='3vw', fontWeight='bolder', lineHeight='normal'), display='flex',
                               flexDirection='column',
                               justifyContent='center', margin='0px', padding='0px', height='40vw', left='5vw', top='calc(7.5%)', color='white', position='absolute'), height='40vw'
                    )), width='100%'),
            pc.vstack(

                pc.divider(orientation='vertical', height='10px'),
                pc.heading('자체 제작된 API로 누구나 쉽게 사용 가능합니다.', width='90%'),
                pc.heading('회원가입 시 1,000 포인트 무료 지급',
                           font_size='xl', width='90%'),
                pc.divider(orientation='vertical', height='10px'),
                pc.hstack(
                    pc.link(
                        pc.button(
                            'FAST-SMS 시작', width='100%', height='50px', color='white', backgroundColor=main_blue),
                        href="/sms",
                        color="rgb(107,99,246)",
                        button=True,
                        width='100%',
                    ),
                    pc.divider(width='10%'),
                    pc.link(
                        pc.button(
                            '결제하기', width='100%', height='50px', color='white', backgroundColor=main_blue),
                        href="/charge",
                        color="rgb(107,99,246)",
                        button=True,
                        width='100%',
                    ),
                    pc.divider(width='10%'),
                    pc.link(
                        pc.button(
                            '상담 문의', width='100%', height='50px', color='white', backgroundColor=main_blue),
                        href="/charge",
                        color="rgb(107,99,246)",
                        button=True,
                        width='100%',
                    ),
                    width='90%'),
                pc.divider(orientation='vertical', height='10px'),
                pc.heading('해외문자 전송시 주의사항', width='90%'),
                pc.text('해외문자 모바일 캠페인에 가입한 사람들을 특별하게 만드세요. 이 그룹에서만 사용할 수 있는 할인 및 제안을 보내십시오. 이것은 그들이 당신의 메시지를 계속 수신하도록 격려하고 아마도 당신의 모바일 마케팅 캠페인으로 새로운 사람들을 끌어들일 것입니다. 이러한 특별 제안이 대상 그룹의 관심사와 관련이 있는지 확인하십시오.', width='90%'),
                pc.text('문자사이트 모바일 마케팅 메시지의 시작 부분에서 회사와 브랜드를 즉시 차단 식별할 수 있는지 확인하십시오. 소비자가 어떤 회사에서 온 것인지 알아보기 위해 전체 텍스트를 읽어야 한다면 짜증이 날 것이고 교활한 마케팅 전략으로 볼 수도 있습니다. 모바일 마케팅을 목표로 삼지 마십시오. 이런 종류의 마케팅에만 의존하면 성공하지 못할 것입니다. 다른 문자받기 기법 중에서도 청중과 소통하는 방법으로 모바일 마케팅에 접근해야 합니다. 이 방법은 특정 고객 그룹에 더 적합할 수 있습니다.', width='90%'),
                pc.text('모든 해외문자 마케터는 모바일 마케팅이 일반적인 마케팅 전략이 아님을 기억해야 합니다. 사실, 그것은 전혀 전략이 아닙니다. 그저 소통의 수단일 뿐입니다. 기본적인 인터넷 마케팅과 같은 모바일 마케팅에 접근하려고 하면 결국 잘 되지 않을 것입니다. 모바일 마케팅의 목표가 무엇인지 이해하고 있는지 확인하세요. 대부분의 사람들에게 이 모바일 접근 방식은 일반적인 접근 방식보다 우선하므로 두 배의 작업이 필요합니다. 그렇기 때문에 시작하기 전에 이 마케팅 분야에서 원하는 것을 정의하는 것이 매우 중요합니다. 이를 통해 캠페인을 보다 효율적으로 간소화할 수 있습니다.', width='90%'),
                pc.text('모바일 마케팅을 통해 정보를 발송할 때는 항상 자신의 이름이나 회사 이름이 눈에 잘 띄고 고객이 가장 먼저 보게 되는지 확인하십시오. 고객이 귀하의 메시지를 읽는 것이 중요하며 스팸이 아님을 알아야 합니다. 모바일 마케팅에 추적 기능을 추가하는 것을 잊지 마십시오! 화면이 작다고 해서 화면이 덜 중요한 것은 아닙니다. 국제문자 모바일 마케팅 캠페인에서 사용 중인 하이퍼링크에 추적 확장을 추가하고 다양한 모바일 전술에 대한 강력한 추적 기능을 제공하는 다양한 모바일 서비스를 살펴보십시오.', width='90%'),),
            pc.accordion(
                pc.accordion_item(
                    pc.accordion_button(
                        pc.heading("안정적인 1:1 전용 게이트웨이 구축"),
                        pc.accordion_icon(),
                    ),
                    pc.accordion_panel(
                        pc.text(
                            "직접 관리중인 플랫폼을 통해 분담 2만개 이상의 SMS 문자를 발송합니다. 업계 최고의 시스템을 이용해보세요."
                        )
                    ),
                ),
                pc.accordion_item(
                    pc.accordion_button(
                        pc.heading("강력한 보안 시스템"),
                        pc.accordion_icon(),
                    ),
                    pc.accordion_panel(
                        pc.text(
                            "DB 관리에 직접 신경쓰는 업체업니다. 최신 AES 보안 알고리즘을 사용하여 관리합니다."
                        )
                    ),
                ),
                pc.accordion_item(
                    pc.accordion_button(
                        pc.heading("업계 최저 건당 발송 비용"),
                        pc.accordion_icon(),
                    ),
                    pc.accordion_panel(
                        pc.text(
                            "길어진 70자 SMS 장문문자 보내기가 가능합니다. 가격대비 효율성이 좋습니다."
                        )
                    ),
                ),
                pc.accordion_item(
                    pc.accordion_button(
                        pc.heading("전송률 99.9% 보장"),
                        pc.accordion_icon(),
                    ),
                    pc.accordion_panel(
                        pc.text(
                            "한번도 발송에 실패한 적이 없습니다. 스팸 차단 성공률, 걱정안하셔도 되고, 문제가 생길시 확인 후환불조치합니다."
                        )
                    ),
                ),
                pc.accordion_item(
                    pc.accordion_button(
                        pc.heading("전업종 문의 받습니다."),
                        pc.accordion_icon(),
                    ),
                    pc.accordion_panel(
                        pc.text(
                            """스팸관련, 불법관련한 사항은 공지사항을 잘 지켜서 문제가  되지 않도록 하시길 바랍니다. 자세한 사항은 문의받습니다.
스마트한 솔루션 및 완벽한 보안을 자랑합니다. 또한 메세지 전송이후 실시간 결과를 제공해드립니다. """
                        )
                    ),
                ),
                pc.divider(orientation='vertical', height='10px'),
                pc.heading('© 2002-2023 FAST.UK Ltd. All rights reserved.',
                           textAlign='center', color='rgba(0,0,0,0.3)', width='100%', font_size='sm', lineHeight='100px'),
                width="90%", fontSize='md'
            )), width='100%')


def db():
    return layout(pc.center(pc.input(on_change=State.set_numberrr), pc.button(on_click=State.get_phonenumber)))


def sms_logo(size: int = 1, photo: int = 1):
    return pc.link(pc.hstack(pc.text('FAST ', fontSize=str(300*size)+'%', textAlign='center', fontWeight='bold'), pc.image(src='/img/FastM.png', width=str(16*size*photo)+'%'), pc.text(' SMS', fontSize=str(300*size)+'%', textAlign='center', fontWeight='bold'),
                             margin=str(2*size)+'%', width='100%', justifyContent='center'), href='/', width='90%')


def sms():
    return pc.center(pc.vstack(

        login(),
        sms_logo(),

        pc.hstack(
            sms_left(),
            sms_right(), width='90%'
        ),
        width='100%', maxWidth='600px'
    ), excel_modal(), width='100%'

    )


def sms_left():
    return pc.vstack(
        pc.vstack(
            pc.text_area(placeholder="SMS subject..", width='100%',
                         height='50vh', resize='none'),
            pc.hstack(pc.button('EXCEL 대량전송', fontWeight='bold', width='50%', margin='3px', on_click=ModalState.excel_modal_show),
                      pc.button('SEND SMS', color='white', fontWeight='bold', backgroundColor=main_blue, width='50%', margin='3px'), width='100%'),
            width='100%'), height='50vh', width='50%'
    )


def sms_right():

    return pc.vstack(
        pc.table(
            pc.thead(
                pc.tr(
                    pc.th(f"Phone Number",
                          width='100%', fontSize='2%', padding='5px'),
                    pc.th()
                ),
                pc.tr(
                    pc.th(pc.text_area(value=State.NumberInput, overflow='hidden', fontSize='2vh', resize='none',
                                       on_change=State.NumberListGet, width='100%', minHeight='5vh', height='5vh', id='numberinput'), padding='1vw', width='70%'),
                    pc.th(pc.button('Add', on_click=State.addNum,
                                    minHeight='5vh', height='4vh', width='100%'), padding='1vw', width='30%'), width='100%'),
            )
        ),
        pc.vstack(
            pc.table(
                pc.thead(
                    pc.foreach(State.NumberZip, lambda x,
                               y: listofnumber(x, y)), height='100%'),
            ), width='100%', margin='0', padding='0', overflow="auto"), height='50vh', width='50%'
    )


class Readexcel(pc.Component):
    library = '../public/reactjs/test.js'
    tag = 'Readexcel'


def charge():
    return pc.center(pc.vstack(
        sms_logo(),
        pc.vstack(
            pc.hstack(
                pc.heading("충전금 결제", size="2xl", color="Grey", width='50%'), pc.divider(width='50%', borderWidth='0px !important'),  width='100%'),
            pc.divider(),
            pc.form_control(
                pc.form_label("가입자 전화번호", html_for="phone_number"),
                pc.input(type_='number', placeholder='010-XXXX-XXXX'),
                pc.form_helper_text('가입 시 사용한 전화번호'),
                is_required=True,
            ),
            pc.form_control(
                pc.form_label("성명", html_for="account_number"),
                pc.input(placeholder='&#xd64d;&#xae38;&#xb3d9;'),
                pc.form_helper_text('무통장 결제 확인에 사용됩니다.'),
                is_required=True,
            ),
            pc.form_control(
                pc.form_label("충전금", html_for="amount"),
                pc.number_input(value=State.charge_price,
                                on_change=State.charge_4x0),
                pc.form_helper_text('1만원 단위로 입력해주세요.'),
                is_required=True,
            ), pc.center(pc.button('무통장 결제'), pc.divider(width='5%', borderWidth='0px'), pc.button('카드 결제'), width='100%'),
            width='90%', marginTop='30px'), pc.heading('© 2002-2023 FAST.UK Ltd. All rights reserved.',
                                                       textAlign='center', color='rgba(0,0,0,0.3)', width='100%', font_size='sm', lineHeight='200px'),))


def layout(component):
    return pc.hstack(
        pc.hstack(
            pc.vstack(
                pc.text('HOT-LINE', fontSize='4vh', fontWeight='bold', background_image="linear-gradient(271.68deg, #EE756A 0.75%, #756AEE 88.52%)",
                        background_clip="text", height='5vh'),
                pc.divider(orientation="vertical", borderWidth='0px'),
                pc.vstack(
                    pc.link(
                        pc.button(
                            'HOME', width='100%', height='4vh', color='white', backgroundColor=main_blue),
                        href="/",
                        color="rgb(107,99,246)",
                        button=True,
                        width='100%',
                    ),


                ),
                pc.divider(orientation="vertical", borderWidth='0px'),
                pc.box(pc.popover(
                    pc.popover_trigger(pc.button(
                        'Contact', height='4vh', marginBottom='10px !important', color='white', backgroundColor=main_blue)),
                    pc.popover_content(
                        pc.popover_body(
                            pc.hstack(
                                pc.tooltip(
                                    pc.image(src='/img/phone_call.png', height='5vh'), label="Call"),
                                pc.divider(),
                                pc.tooltip(
                                    pc.image(src='/img/telegram.png', height='5vh'), label="Telegram"),
                                pc.divider(),
                                pc.tooltip(
                                    pc.image(src='/img/telegram.png', height='5vh'), label="Telegram")),
                            width='100%'

                        ), width='25vh', marginLeft='50px'
                    ),
                )), width='20vw', height='100vh', padding='0px', margin='0px'
            ), pc.divider(orientation="vertical",
                          borderColor='rgba(200,200,200,1)', borderWidth='1px'), height='100vh', position='fixed'), pc.box(component, marginLeft='21vw !important', width='80vw', height='100vh'), padding='0px', margin='0px',  width='100%', height='100vh')


app = pc.App(state=State)
app.add_page(index, path='/', title="FAST-SMS")
app.add_page(sms, path='/sms', title="FAST-SMS")
app.add_page(charge, path='/charge', title="FAST-SMS")
app.compile()
