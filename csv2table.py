import pandas as pd
import os

# Load the CSV file
def generate_latex_tables(file_path):
    # Read CSV file
    data = pd.read_csv(file_path)

    # Capitalize the first letter of "画像名"
    data["画像名"] = data["画像名"].str.capitalize()

    # Append "mm" to 撮影距離 values
    data["撮影距離"] = data["撮影距離"].astype(str) + "mm"
    # Convert 正解率 to integers and append "%"
    data["正解率"] = data["正解率"].fillna(0).astype(float).round(0).astype(int).astype(str) + "\%"   

    # Group by 'ビット数'
    grouped = data.groupby('ビット数')

    # Ensure output directory exists
    output_dir = 'latex_tables'
    os.makedirs(output_dir, exist_ok=True)

    # Generate a LaTeX table for each group
    for bit_count, group in grouped:
        # Prepare the data for the desired layout
        distances = sorted(group["撮影距離"].unique())
        formatted_data = []

        for name, sub_group in group.groupby("画像名"):
            max_rows = sub_group.shape[0]
            for i in range(max_rows):
                row = [name if i == 0 else ""]
                row_empty = True
                for distance in distances:
                    match = sub_group[sub_group["撮影距離"] == distance]
                    if not match.empty and i < len(match):
                        row.extend([distance, match.iloc[i]["アルファ値"], match.iloc[i]["正解率"]])
                        row_empty = False
                    else:
                        row.extend(["", "", ""])
                if not row_empty:
                    formatted_data.append(row)

        # Create a DataFrame for LaTeX output
        columns = ["画像名"]
        for distance in distances:
            columns.extend(["撮影距離", "アルファ値", "正解率"])
        formatted_df = pd.DataFrame(formatted_data, columns=columns)

        # Create LaTeX table with grid lines
        column_format = '|l|' + ''.join(['c|c|r|' for _ in distances])
        latex_table = formatted_df.to_latex(
            index=False,
            header=True,
            escape=False,
            longtable=False,
            column_format=column_format
        )

        # Add horizontal lines for grid
        latex_table = latex_table.replace('\\toprule', '\\hline')
        latex_table = latex_table.replace('\\midrule', '\\hline')
        latex_table = latex_table.replace('\\bottomrule', '\\hline')
        latex_table = latex_table.replace('アルファ', 'α')
        latex_table = latex_table.replace('Milk', 'Milkdrop')
        latex_table = latex_table.replace('.0', '')
        latex_table = latex_table.replace('撮影距離', '距離')

        # Define output file name
        output_file = os.path.join(output_dir, f"table_bit_{bit_count}.txt")

        # Write to text file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(latex_table)

        print(f"Generated LaTeX table for ビット数={bit_count}: {output_file}")

# Path to the input CSV file
csv_file_path = 'output.csv'

# Generate LaTeX tables
generate_latex_tables(csv_file_path)