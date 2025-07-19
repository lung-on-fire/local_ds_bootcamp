import sys
import os
import config
from analytics import Research

def main():
    try: 
        if len(sys.argv) != 2 or not os.path.exists(sys.argv[1]) or not os.path.isfile(sys.argv[1]):
            raise ValueError("No such file in directory")
        
        else:
            research = Research()
            data = research.file_reader()
            calculations = Research.Calculations(data)
            analytics = Research.Analytics(data)

            heads, tails = calculations.counts()
            heads_perc, tails_perc = calculations.fractions(heads, tails)
            predictions = analytics.predict_random(config.num_of_steps)
            pred_num_tails = 0 
            pred_num_heads = 0

            for pred in predictions:
                if pred == [0,1]:
                    pred_num_tails += 1
                else:
                    pred_num_heads += 1

            report_data = config.report.format(
            total_observations=len(data),
            tails=tails,
            heads=heads,
            tails_percentage=round(tails_perc, 2),
            heads_percentage=round(heads_perc, 2),
            num_of_steps=config.num_of_steps ,
            pred_num_tails = pred_num_tails,
            pred_num_heads = pred_num_heads)

            analytics.save_file(report_data, 'report', 'txt')
            research.send_telegram_message()

            print(report_data)

    except Exception as error:
        print(f'Error! {error}')
        sys.exit(1)

if __name__ == '__main__':
    main()
