import flet as ft
import datetime
from random import randint, choice
import pyperclip

def main(page: ft.Page):
    
    def theme_changed(e):
        page.theme_mode = (
            ft.ThemeMode.DARK
            if page.theme_mode == ft.ThemeMode.LIGHT
            else ft.ThemeMode.LIGHT
        )
        themeBT.icon = (
            ft.icons.LIGHT_MODE  if page.theme_mode == ft.ThemeMode.LIGHT else ft.icons.DARK_MODE
        )
        themeBT.tooltip = (
            "Use dark mode"  if page.theme_mode == ft.ThemeMode.LIGHT else "Use light mode"
        )
        page.update()

    def FillTheBin(e):
        c_len = "xxxxxxxxxxxxxxxx"
        temp_bin_var = (binTF.value).upper().replace(" ","")
        ex_bin = (temp_bin_var + ("x" * (len(c_len)-len(temp_bin_var)) ) )
        binTF.value = (ex_bin.lower())
        page.update()
    
    def Generate(e):
        cc_gend = ""
        cheCcTF.value = ""
        c_len = "xxxxxxxxxxxxxxxx"
        temp_bin_var_for_use = binTF.value.upper().replace(" ","")
        temp_bin_var = binTF.value.upper().replace("X","").replace(" ","")
        if ( not temp_bin_var.isdigit() or ( len(binTF.value.replace(" ","")) > len(c_len) or len(temp_bin_var) >= len(c_len) ) ) and temp_bin_var_for_use != "XXXXXXXXXXXXXXXX":
            binTF.error_text = error_text[0]
            pass
        elif (not cvvTF.value.isdigit() and cvvTF.value.replace(" ","") != "") or not len(cvvTF.value) in range(4):
            cvvTF.error_text = error_text[1]
        elif not quantityTF.value.replace(" ","").isdigit() or (quantityTF.value.replace(" ","") != "" and int(quantityTF.value.replace(" ","")) <= 0):
            quantityTF.error_text = error_text[2]
        else:
            binTF.error_text = None
            cvvTF.error_text = None
            quantityTF.error_text = None
            month = list(months).index(monthDD.value)
            year = yearDD.value

            #card generation
            temp_bin_var_for_use = temp_bin_var_for_use.lower()
            ex_bin = (temp_bin_var_for_use + ("x" * (len(c_len)-len(temp_bin_var_for_use)) ) )

            for q in range(int(quantityTF.value)):
                ch = ""
                for char in ex_bin:
                    if char == "x":
                        ch += str(randint(0,9))
                    else:
                        ch += char
                gen_card = ch
                
                
                #month generation
                if monthDD.value == "Random":
                    temp_mm = list(months)
                    temp_mm.pop(0)
                    mm_choix = choice(temp_mm)
                    mm = temp_mm.index(mm_choix) + 1 
                    
                    if len(str(mm)) < 2:
                        mm = "0"+str(mm)
                
                else:
                    mm = (list(months).index(monthDD.value))
                    if len(str(mm)) < 2:
                        mm = "0"+str(mm)
                
                #year generation
                if yearDD.value == "Random":
                    temp_yy = list(years)
                    temp_yy.pop(0)
                    yy = choice(temp_yy)
                else:
                    yy = yearDD.value
                
                #cvv generation
                if cvvTF.value.replace(" ","") == "":
                    cvv = randint(100,999)
                else:
                    cvv_temp = cvvTF.value.replace(" ","")
                    ex_cvv = (cvv_temp + ("x" * (3-len(cvv_temp)) ) )
                    
                    ch = ""
                    for char in ex_cvv:
                        if char == "x":
                            ch += str(randint(0,9))
                        else:
                            ch += char
                    cvv = ch
                
                gen = f"{gen_card}|{mm}|{yy}|{cvv}"
                cc_gend += f"{gen}\n"
            
            cheCcTF.value = Check(cc_gend.split('\n'))
            ccnb = 0
            if cheCcTF.value != "":
                ccnb = len(cheCcTF.value.split('\n')) - 1
                if ccnb == 1 and int(quantityTF.value) == 1:
                    page.snack_bar.content = ft.Text(f"{ccnb} valid card from 1 card", color=ft.colors.WHITE)
                else:
                    page.snack_bar.content = ft.Text(f"{ccnb} valid card from {quantityTF.value} cards", color=ft.colors.WHITE)
            else:
                if ccnb == 0 and int(quantityTF.value) == 1:
                    page.snack_bar.content = ft.Text(f"0 valid card from 1 card", color=ft.colors.WHITE)
                elif ccnb == 0 and int(quantityTF.value) > 1:
                    page.snack_bar.content = ft.Text(f"0 valid card from {quantityTF.value} cards", color=ft.colors.WHITE)

            page.snack_bar.open = True
                
        page.update()

    def Check(cards_text):
        chkd_cc =  ""
        for _ in range(2):
            cards_text.pop(-1)
        for card in cards_text:
            chkd_cc += CheckCard(card)
        return chkd_cc

    def CheckCard(card):
        card_nbr = card.split("|")[0]
        inp_nbr = 0
        pr_nbr = 0
        chkd_cc = ""
        for i in range(len(card_nbr)):
            if i%2 != 0:
                inp_nbr += int(card_nbr[i])
            else:
                if int(card_nbr[i])*2 < 10:
                    pr_nbr += (int(card_nbr[i])*2)
                else:
                    nbr = (str(int(card_nbr[i])*2))
                    for j in nbr:
                        pr_nbr += int(j)
        if (inp_nbr + pr_nbr)%10 == 0:
            chkd_cc += f"{card}\n"
        return chkd_cc

    def CopyToclipboard(e):
        if cheCcTF.value != "":
            pyperclip.copy(cheCcTF.value)
            page.snack_bar.content = ft.Text(f"Copied", color=ft.colors.WHITE)
            page.snack_bar.open = True
            page.update()

    page.title = "CC master by Hama BTW"
    page.horizontal_alignment = "center"
    page.scroll = "adaptive"

    error_text = ["Error in the bin forme","Error in the cvv forme","Error quantity, must be a degit and can't be negative or 0"]

    #theme button
    page.theme_mode = ft.ThemeMode.DARK
    themeBT = ft.IconButton(icon=ft.icons.DARK_MODE, on_click=theme_changed, tooltip="Use light mode", expand=1)

    #app title
    app_title = ft.Text(value="CC master by Hama BTW", expand=3, text_align="center", size=32)
  

    #Bin Input Field
    binTF = ft.TextField(label="Bin", hint_text="Please enter the bin here", autofocus=True, expand=2, focused_border_color=ft.colors.PINK, on_blur=FillTheBin)

    #Month Input Field
    months = ("Random","January (1)","February (2)","March (3)","April (4)","May (5)","June (6)","July (7)","August (8)","September (9)","October (10)","November (11)","December (12)")
    monthDD = ft.Dropdown(
            label="Month",
            hint_text="Choose the month",
            value="Random",
            width=150,
            expand=1,
            focused_border_color=ft.colors.PINK
        )
    for month in months:
        monthDD.options.append(ft.dropdown.Option(month))

    #year Input Field
    years = ["Random"]
    this_year = datetime.datetime.now().year
    for i in range(this_year, this_year+9):
        years.append(str(i))
    years = tuple(years)

    yearDD = ft.Dropdown(
            label="Year",
            hint_text="Choose the year",
            value="Random",
            width=150,
            expand=1,
            focused_border_color=ft.colors.PINK,
        )
    for year in years:
        yearDD.options.append(ft.dropdown.Option(year))
    
    #Cvv Input Field
    cvvTF = ft.TextField(label="Cvv", hint_text="Please enter the cvv here", width=150, expand=1, focused_border_color=ft.colors.PINK)

    #Quantity Input Field
    quantityTF = ft.TextField(label="Quantity", hint_text="Please enter the credit cards quantity here", value="100", width=150, expand=1, focused_border_color=ft.colors.PINK)

    #Check button
    CheCcBT = ft.ElevatedButton(text="Check",
        on_click=Generate,
        width=140, 
        expand=1,
        style=ft.ButtonStyle(
            bgcolor=ft.colors.PINK_ACCENT_200,
            color=ft.colors.WHITE
        )
    ) 

    #Checked credit cards
    cheCcTF =  ft.TextField(label="Checked credit cards", multiline=True, min_lines=10, max_lines=10, focused_border_color=ft.colors.PINK, read_only=True)


    #copy icon button
    cpyIcCheCcBT = ft.IconButton(
                    icon=ft.icons.CONTENT_COPY,
                    icon_color=ft.colors.PINK,
                    icon_size=20,
                    tooltip="Copy",
                    right=0,
                    bottom=0,
                    on_click=CopyToclipboard)
    
    #Checked cards Zone
    CheckCcZone = ft.Stack([cheCcTF, cpyIcCheCcBT], expand=3)

    #snack bar
    page.snack_bar = ft.SnackBar(
        content=ft.Text(" "),
        action="Alright!",
        bgcolor=ft.colors.PINK_ACCENT_200,
        action_color=ft.colors.WHITE
    )


    page.add(
        ft.Row([app_title, themeBT]),
        ft.Row([binTF, monthDD, yearDD]),
        ft.Row([cvvTF, quantityTF, CheCcBT]),
        ft.Row([CheckCcZone])
    )

    page.update()

ft.app(target=main)


