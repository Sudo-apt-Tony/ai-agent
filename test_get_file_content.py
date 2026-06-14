from functions.get_file_content import get_file_content

result_lorem = get_file_content("calculator", "lorem.txt")
print("lorem.txt metadata:")
print(f'\tlorem.txt length: "{len(result_lorem)}"')
print(f"\tlorem.txt truncated: {'truncated' in result_lorem}\n")

result_main = get_file_content("calculator", "main.py")
print(f"main.py result:\n\n{result_main}\n")

result_calc = get_file_content("calculator", "pkg/calculator.py")
print(f"calculator.py result:\n\n{result_calc}\n")

result_bin = get_file_content("calculator", "/bin/cat")
print(f"/bin/cat result: \n\t{result_bin}\n")

result_dne = get_file_content("calculator", "pkg/does_not_exist.py")
print(f"pkg/does_not_exist.py result:\n\t{result_dne}\n")
