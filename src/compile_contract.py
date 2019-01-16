from solc import compile_files


# compile all contract files
contracts = compile_files(['contract/structures.sol', 'contract/bibliography.sol'])

print(contracts)
