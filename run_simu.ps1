# run "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass" before executing this script

# Define file paths
$f1 = "1d_Rac_dynamics.py"
$f2 = "simu_para.py"

# Loop through values for x_var
For ($y_var = 1; $y_var -le 2; $y_var++){ # running time of datasets

	New-Item -Name ".\data\120924_$y_var" -ItemType Directory
	
	# Read the content of f_2.py
   	$content = Get-Content -Path $f2
    
    	# Replace the value of x_var in f_2.py
    	$newContent = $content -replace "(?<=dataset_number_int\s*=\s*)\d+", $y_var
    
    	# Write the updated content back to f_2.py
    	Set-Content -Path $f2 -Value $newContent

	For ($x_var = 1; $x_var -le 15; $x_var++) {
    		# Read the content of f_2.py
    		$content = Get-Content -Path $f2
    
    		# Replace the value of x_var in f_2.py
    		$newContent = $content -replace "(?<=data_number_int\s*=\s*)\d+", $x_var
    
    		# Write the updated content back to f_2.py
    		Set-Content -Path $f2 -Value $newContent
    
    		# Run f_1.py
   		 python $f1
	}
}
