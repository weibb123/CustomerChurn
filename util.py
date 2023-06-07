import numpy as np
import pandas as pd

def transform_data(test_df, col_order, mean_eve_mins, onehot):
    
    x = test_df.copy()

    # re doing everything done on train set but on test set
    x['area_code'] = x['area_code'].fillna('missing')
    x['voice_mail_plan'] = x['voice_mail_plan'].fillna('missing')
    x['total_eve_minutes_missing'] = x['total_eve_minutes'].isnull().astype(int)
    x['total_eve_minutes'] = x['total_eve_minutes'].fillna(mean_eve_mins)

    # FE - Ratios
    x['day_ratio'] = x['total_day_charge'] / x['total_day_minutes']
    x['eve_ratio'] = x['total_eve_charge'] / x['total_eve_minutes']
    x['night_ratio'] = x['total_night_charge'] / x['total_night_minutes']
    x['intl_ratio'] = x['total_intl_charge'] / x['total_intl_minutes']
    x = x.drop(['total_day_charge', 'total_eve_charge', 'total_night_charge',
            'total_intl_charge', 'total_day_minutes', 'total_eve_minutes',
            'total_night_minutes', 'total_intl_minutes'], axis=1)

    # FE - Log transform
    x['number_customer_service_calls'] = np.log(x['number_customer_service_calls'] + 1)

    # FE - Unhappy customers
    x['promotions_offered'] = x['promotions_offered'].replace(['NO', np.NaN], 'No')
    x['unhappy_customers'] = ((x.remaining_term < 5) & 
                              (x.last_nps_rating <= 7) &
                              (x.promotions_offered == 'No')).astype(int)
    
    # Onehot encoder
    encoded_columns = onehot.transform(x.select_dtypes(include='object')).toarray()
    x = x.select_dtypes(exclude='object')
    x[onehot.get_feature_names_out()] = encoded_columns

    return x[col_order]