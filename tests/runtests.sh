#!/bin/bash

rm -f test[0-9][0-9][0-9].v
rm -f test[0-9][0-9][0-9]_*.log

set -e

run() {
	idx=0 id=$id
	echo -n "Checking ${id}.."

	PYTHONPATH=".." python3 ${id}.py

	yosys_q="-q"
	if $verbose; then
		yosys_q=""
	fi

	while read tag stmt args; do
		(( ++idx ))
		read a1 a2 a3 a4 a5 < <( echo $args; )
		case "$stmt" in
			test-sat-equiv-induct)
				yosys $yosys_q -l ${id}_${idx}.log -p "read_verilog ${id}.v; prep" \
					-p "miter -equiv -ignore_gold_x -flatten -make_outputs $a1 $a2 miter" \
					-p "sat -verify -prove trigger 0 -show-ports -tempinduct -set-init-undef -set-def-inputs -maxsteps $a3 miter"
				;;
			test-sat-equiv-bmc)
				yosys $yosys_q -l ${id}_${idx}.log -p "read_verilog ${id}.v; prep; memory_map;;" \
					-p "miter -equiv -ignore_gold_x -flatten -make_outputs $a1 $a2 miter" \
					-p "sat -verify -prove trigger 0 -show-ports -set-init-undef -set-def-inputs -seq $a3 miter"
				;;
			test-sat-equiv-comb)
				yosys $yosys_q -l ${id}_${idx}.log -p "read_verilog ${id}.v; prep; memory_map;;" \
					-p "miter -equiv -ignore_gold_x -flatten -make_outputs $a1 $a2 miter" \
					-p "sat -verify -prove trigger 0 -show-ports -set-def-inputs miter"
				;;
			*)
				echo "Unsupported test stmt: $tag $stmt $args"
				exit 1
				;;
		esac
		echo -n " ok_$idx"
	done < <( grep '^//@' ${id}.v; )
	echo
}

verbose=false
if [ "$1" = "-v" ]; then
	verbose=true
	shift
fi

if [ $# = 0 ]; then
	for id in test[0-9][0-9][0-9].py; do
		id=${id%.py}
		run $id
	done
else
	for id; do
		run $id
	done
fi

echo "ALL OK"
