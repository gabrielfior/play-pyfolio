class BuyAndHold_More_Fund(bt.Strategy):
    # ToDo - Add etf allocation to init method
    params = dict(
        monthly_cash=700.0,  # amount of cash to buy every month
    )

    def start(self):
        # Activate the fund mode and set the default value at 100
        self.broker.set_fundmode(fundmode=True, fundstartval=100.00)
        self.cash_start = self.broker.get_cash()
        self.val_start = 100.0

        # Add a timer which will be called on the 1st trading day of the month
        self.add_timer(
            bt.timer.SESSION_END,  # when it will be called
            monthdays=[1],  # called on the 1st day of the month
            monthcarry=True,  # called on the 2nd day if the 1st is holiday
        )

    def buy_fixed_cash_amount(self, target_value, data_name):
        data_feed = self.getdatabyname(name=data_name)
        size = round(target_value / data_feed.close, 2)
        print('buying size {} of data {}, target_value {}'.format(size, data_name, target_value))
        return self.buy(exectype=bt.Order.Market, size=size, data=data_feed)

    def notify_timer(self, timer, when, *args, **kwargs):
        # Add the influx of monthly cash to the broker
        self.broker.add_cash(self.p.monthly_cash)

        # buy available cash
        target_value = self.broker.getcash() + self.p.monthly_cash
        # self.buy_fixed_cash_amount(target_value,'vusa')

        # follow asset allocation
        order_list = []
        for data_name, (data_feed, percent_allocation) in etf_allocation_csv.items():
            target = target_value * percent_allocation
            print('buying {} from {} when {}, total target {}'.format(target, data_name, when, target_value))
            order = self.buy_fixed_cash_amount(target, data_name)
            if not order:
                print('could not buy from {} when {}'.format(data_name, when))

        # self.order_target_value(target=target_value/2, data='vusa')
        # self.order_target_value(target=target_value/2, data='stoxx')

    def stop(self):
        # calculate the actual returns
        self.roi = (self.broker.get_value() / self.cash_start) - 1.0
        self.froi = self.broker.get_fundvalue() - self.val_start
        print('ROI:        {:.2f}%'.format(100.0 * self.roi))
        print('Fund Value: {:.2f}%'.format(self.froi))
        print('broker fund value {} broker val start {}'.format(self.broker.get_fundvalue(), self.val_start))
