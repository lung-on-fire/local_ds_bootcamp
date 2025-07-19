import sys
import resource

def main():
    if len(sys.argv) !=2:
        print("Usage: ordinary.py filepath")
        sys.exit(1)
    else:
        filepath = sys.argv[1]
        lines = read_file_lines(filepath)

        start_res_usage = resource.getrusage(resource.RUSAGE_SELF)
        for line in lines:
            pass
        end_res_usage = resource.getrusage(resource.RUSAGE_SELF)

        peak_mem_usage_gb = end_res_usage.ru_maxrss / (1024 ** 3)
        user_mode_time = end_res_usage.ru_utime - start_res_usage.ru_utime
        system_mode_time = end_res_usage.ru_stime - start_res_usage.ru_stime
        total_time = user_mode_time + system_mode_time

        print(f"Peak Memory Usage = {peak_mem_usage_gb:.5f} GB")
        print(f"User Mode Time + System Mode Time = {total_time:.5f}s")

def read_file_lines(filepath):
        try:
            with open(filepath, "r") as file:
                lines = file.readlines()
            return lines
        
        except Exception as error:
            print(f"Error! {error}")
            sys.exit(1)



if __name__== '__main__':
    main()


#python3 ordinary.py ../../datasets/ml-25m/ratings.csv
#../../datasets/ml-25m/ratings.csv