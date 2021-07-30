
from datetime import datetime

import bootwrap as bw

# ------------------------------------------------------------------------------
# Web-components for handling SHARES
# ------------------------------------------------------------------------------


class ShareDialog(bw.Dialog):
    def __init__(self, action, sid, company, nos):
        # Defines dialog actions.
        wc_cancel = bw.Button('Cancel').add_classes('float-right').dismiss()
        wc_confirm = bw.Button('Confirm').add_classes(
            'float-right').mr(2).as_success().submit()

        super().__init__(
            f'{action.capitalize()} "{company}" Shares',
            bw.Form(
                bw.NumericInput(
                    'Number of Shares',
                    'nos',
                    placeholder=f'number of to {action} (0<n<={nos})'
                ),
                wc_cancel,
                wc_confirm
            ).on_submit(f'portfolio/buy/{sid}')
        )


class BuyShareDialog(ShareDialog):
    def __init__(self, share, user):
        # Gets the number of shares a user is allowed to buy.
        nos = int(user.balance / share.price)

        # Initializes a buy action dialog window.
        super().__init__('buy', share.id, share.company, nos)


class SellShareDialog(ShareDialog):
    def __init__(self, share, user):
        # Gets the number of shares a user is allowed to sell.
        record = user.get_record(share.id)
        nos = record.nos

        # Initializes a sell action dialog window.
        super().__init__('buy', share.id, share.company, nos)


class ShareCard(bw.Deck.Card):
    def __init__(self, share, user, wc_buy_dialog):
        super().__init__(
            bw.Panel(
                bw.Text(f'NASDAQ: {share.id}').as_strong(),
                bw.Text('$%.2f' % share.price).as_heading(3).as_success().
                add_classes('float-right')
            ),
            description=bw.Panel(
                bw.Text(share.company).as_heading(3).as_primary(),
                bw.Text(share.description)
            ),
            figure=bw.Image(
                f'{share.id.lower()}-logo.png', width=128).mt(3),
            marker=datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        )

        self.add_menu(
            bw.Button("Buy").toggle(wc_buy_dialog)
        )

        self.link(share.url)


class ShareItem(bw.List.Item):
    def __init__(self, share, user, wc_sell_dialog):
        record = user.get_record(share.id)
        nos = record.nos
        investment = record.investment

        wc_description = None
        if nos == 1:
            wc_description = bw.Text(f'1 share of {share.company}')
        else:
            wc_description = bw.Text(f'{nos} shares of {share.company}')
        wc_description.as_muted()

        wc_figure = bw.Image(
            f'{share.id.lower()}-logo.png', width=32, height=32
        )

        super().__init__(
            f'NASDAQ: {share.id}',
            description=wc_description,
            figure=wc_figure
        )

        avg_pps = investment / float(nos)
        cur_pps = share.price

        gain = (max(avg_pps, cur_pps) / min(avg_pps, cur_pps)) *\
            (+1.0 if cur_pps > avg_pps else -1.0)

        wc_gain = None
        if gain > 0:
            wc_gain = bw.Text('+%.2f%%' % gain).as_success().as_small()
        else:
            wc_gain = bw.Text('%.2f%%' % gain).as_danger().as_small()

        wc_sell = bw.Button("Sell").toggle(wc_sell_dialog).as_primary()

        self.add_menu(
            bw.Panel(
                bw.Text('$%.2f' % (nos * share.price)).as_strong(),
                wc_gain
            ).vertical().mr(2),
            wc_sell
        )

# ------------------------------------------------------------------------------
# Web-components for handling user ACCOUNT
# ------------------------------------------------------------------------------


class UserAccountCard(bw.Deck.Card):
    def __init__(self, user, view=True):
        wc_deposit_dialog = bw.Dialog(
            'Deposit Money',
            bw.Form(
                bw.NumericInput(
                    'Amount($)',
                    'amount',
                    placeholder='amount to deposit'
                ),
                bw.Button('Cancel').add_classes('float-right').dismiss(),
                bw.Button('Confirm').add_classes('float-right').mr(2).
                as_success().
                submit()
            ).on_submit('account/deposit')
        )

        wc_withdraw_dialog = bw.Dialog(
            'Withdraw Money',
            bw.Form(
                bw.NumericInput(
                    'Amount($)',
                    'amount',
                    placeholder=f'amount to withdraw (<{user.balance})'
                ),
                bw.Button('Cancel').add_classes('float-right').dismiss(),
                bw.Button('Confirm').add_classes('float-right').mr(2).
                as_success().
                submit()
            ).on_submit('account/withdraw')
        )

        super().__init__(
            bw.Panel(
                bw.Text('Your Balance').as_strong(),
                bw.Text('$%.2f' % user.balance).as_heading(3).
                add_classes('float-right')
            ),
            description=bw.Panel(
                bw.Text('Account number: 12345678').as_paragraph(),
                bw.Text('Sort code: 12-34-56').as_paragraph(),
                wc_deposit_dialog,
                wc_withdraw_dialog
            ),
            figure=bw.Image('bank.png', width=128).mt(3),
            marker=datetime.now().strftime("%d-%b-%Y %H:%M:%S")
        )

        if not view:
            self.add_menu(
                bw.Button("Deposit").toggle(wc_deposit_dialog).as_primary(),
                bw.Button("Withdraw").toggle(wc_withdraw_dialog).as_secondary()
            )

# ------------------------------------------------------------------------------
# Web-components for handling user ACTIVITIES
# ------------------------------------------------------------------------------


class ActivityTable(bw.Table):
    def __init__(self, user):
        head, body = user.get_activity()
        super().__init__(head, body)

        def get_icon(target):
            if target == 'account':
                return bw.Image('cash.png', width=32, height=32)
            return bw.Image('stock.png', width=32, height=32)

        def get_style(action):
            if action in ['deposit', 'sell']:
                return 'text-success'
            return 'text-danger'

        self.body.transform(
            0,
            bw.TableEntity.VALUE,
            lambda timestamp: timestamp.strftime("%m/%d/%Y, %H:%M:%S")
        )

        self.body.transform(
            1,
            bw.TableEntity.VALUE,
            lambda target: get_icon(target)
        )

        self.body.transform(
            2,
            bw.TableEntity.ROW,
            lambda action: get_style(action)
        )

        self.body.transform(
            0,
            bw.TableEntity.CELL,
            lambda timestamp: 'text-muted'
        )
        self.body.transform(
            2,
            bw.TableEntity.CELL,
            lambda timestamp: 'text-dark font-weight-bold'
        )
