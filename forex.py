import requests
import numpy as np


class ForexRequest:
    __usd_cad_status = False
    __corra_status = False
    __usd_cad_json = None
    __corra_json = None
    __usd_cad_result = None
    __corra_result = None

    @classmethod
    def get_usd_cad(cls, start_date, end_date):
        try:
            url = f"https://www.bankofcanada.ca/valet/observations/FXUSDCAD?" \
                      f"start_date={start_date}&end_date={end_date}"
            request = requests.get(url)
            cls.__usd_cad_json = request.json()
            cls.__usd_cad_status = True
            return True
        except Exception:
            return False

    @classmethod
    def get_corra(cls, start_date, end_date):
        try:
            url = f"https://www.bankofcanada.ca/valet/observations/AVG.INTWO?" \
                      f"start_date={start_date}&end_date={end_date}"
            request = requests.get(url)
            cls.__corra_json = request.json()
            cls.__corra_status = True
            return True
        except Exception:
            return False

    @classmethod
    def create_usd_cad_list(cls):
        if cls.__usd_cad_status and cls.__corra_result is None:
            cls.__usd_cad_result = []
            for day in cls.__usd_cad_json['observations']:
                rate = float(day['FXUSDCAD']['v'])
                cls.__usd_cad_result.append(rate)

    @classmethod
    def create_corra_list(cls):
        if cls.__corra_status and cls.__corra_result is None:
            cls.__corra_result = []
            for day in cls.__corra_json['observations']:
                rate = float(day['AVG.INTWO']['v'])
                cls.__corra_result.append(rate)

    # Needed due to inconsistency in data dates.
    @classmethod
    def __create_corr_lists(cls):
        if cls.__usd_cad_status and cls.__corra_status:
            len_1 = len(cls.__usd_cad_result)
            len_2 = len(cls.__corra_result)
            if len_1 == len_2:
                return

            counter_1 = 0
            counter_2 = 0
            lst_1 = []
            lst_2 = []
            while counter_1 < max(len_1, len_2) and counter_2 < max(len_1,
                                                                    len_2):
                try:
                    date_1 = cls.__usd_cad_json['observations'][counter_1]['d']
                    date_2 = cls.__corra_json['observations'][counter_2]['d']
                except IndexError:
                    break

                if date_1 == date_2:
                    lst_1.append(float(cls.__usd_cad_json['observations']
                                       [counter_1]['FXUSDCAD']['v']))
                    lst_2.append(float(cls.__corra_json['observations']
                                       [counter_1]['AVG.INTWO']['v']))
                    counter_1 += 1
                    counter_2 += 1
                elif len_1 > len_2:
                    counter_1 += 1
                else:
                    counter_2 += 1
            cls.__usd_cad_result = lst_1
            cls.__corra_result = lst_2

    @classmethod
    def get_high(cls, is_corra):
        if is_corra:
            return max(cls.__corra_result)
        else:
            return max(cls.__usd_cad_result)

    @classmethod
    def get_low(cls, is_corra):
        if is_corra:
            return min(cls.__corra_result)
        else:
            return min(cls.__usd_cad_result)

    @classmethod
    def get_avg(cls, is_corra):
        if is_corra:
            return sum(cls.__corra_result) / len(cls.__corra_result)
        else:
            return sum(cls.__usd_cad_result) / len(cls.__usd_cad_result)

    @classmethod
    def get_correlation(cls):
        cls.__create_corr_lists()
        x_avg = cls.get_avg(False)
        y_avg = cls.get_avg(True)
        numerator = 0
        denom_1 = 0
        denom_2 = 0

        for x, y in zip(cls.__usd_cad_result, cls.__corra_result):
            numerator += (x - x_avg) * (y - y_avg)
            denom_1 += pow((x - x_avg), 2)
            denom_2 += pow((y - y_avg), 2)

        if pow(denom_1 * denom_2, 1/2) < 0.000000001 and numerator < 0.000000001:
            return np.nan
        else:
            return numerator / pow(denom_1 * denom_2, 1/2)

    @classmethod
    def reset_class(cls):
        cls.__usd_cad_status = False
        cls.__corra_status = False
        cls.__usd_cad_json = None
        cls.__corra_json = None
        cls.__usd_cad_result = None
        cls.__corra_result = None
