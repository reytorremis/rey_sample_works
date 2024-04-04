const calculator = document.querySelector('.calculator')
const keys = calculator.querySelector('.calculator__keys')
const display = document.querySelector('#calculator-display')
// let memory = document.getElementById("calculator_memory").value;
let memorylist = [];
// const memorycheck = memory? memory : '';
    
const calculate = (n1, operator, n2) => {
  if (operator === 'add') return parseFloat(n1) + parseFloat(n2)
  if (operator === 'subtract') return parseFloat(n1) - parseFloat(n2)
  if (operator === 'multiply') return parseFloat(n1) * parseFloat(n2)
  if (operator === 'divide') return parseFloat(n1) / parseFloat(n2)
   }

function return_whole_number (x) {
  console.log(Number.isInteger(x))
  if (Math.round(parseFloat(x)*100)/100 - parseInt(x) > 0) {
    return parseFloat(x).toFixed(2)
  } else {
    return parseInt(x)
  }
}


function return_corresponding_symbol (action) {
  if (action === 'add') return '+'
  if (action === 'subtract') return '-'
  if (action === 'multiply') return 'x'
  if (action === 'divide') return String.fromCharCode(247)
   }


function aggregate_memory (params) {
  let x1 = null;
  let op = null;
  console.log(params)
    for (i=0; i < params.length; i++) {
       try {
         if (i === 0){
          x1  = parseFloat(params[i]);
         } else if (i % 2 === 1) {
            op = params[i]
           }
          else if (i % 2 === 0 && i !== 0) {
            if (op === "+"){
             return x1 + parseFloat(params[i]);
           } else if (op === "-"){
             return x1 - parseFloat(params[i]);
           } else if (op === "x"){
             return x1 * parseFloat(params[i]);
           } else if (op === String.fromCharCode(247)){
             return x1 / parseFloat(params[i]);
           }
         }
       }
       catch {
         op = params[i]
       }
}
}

keys.addEventListener('click', e => {
  if (e.target.matches('button')) {
    const key = e.target
    const action = key.dataset.action
    const keyContent = key.textContent
    const displayedNum = display.textContent
    const previousKeyType = calculator.dataset.previousKeyType
    const memoryupdate = []
    // console.log(memorylist)
    // console.log(previousKeyType)

if (!action) {
 if (
    displayedNum === '0' ||
    previousKeyType === 'operator' ||
    previousKeyType === 'calculate'
  ) 
  {
    display.textContent = keyContent
  } else {
    display.textContent = displayedNum + keyContent
      }
    calculator.dataset.previousKeyType = 'number'
  } else if (action === 'clear-ce') {
    display.textContent = 0
    calculator.dataset.previousKeyType = 'clear'
  } else if (action === 'clear-ac') {
    display.textContent = 0;
    calculator.dataset.firstValue = '';
    calculator.dataset.modValue = '';
    calculator.dataset.operator = '';
    calculator.dataset.previousKeyType = '';
    memorylist = [];
    document.getElementById("calculator-memory").innerHTML = null;
    calculator.dataset.previousKeyType = 'clear'
  }
  else if (
      action === 'add' ||
      action === 'subtract' ||
      action === 'multiply' ||
      action === 'divide' 
  ) {
      
      const firstValue = calculator.dataset.firstValue
      const operator = calculator.dataset.operator
      const secondValue = displayedNum
      if (firstValue && operator && previousKeyType !== 'operator' && previousKeyType !== 'calculate') {
        if (!memorylist[0]){
          memorylist.push(firstValue)
          memorylist.push(return_corresponding_symbol(operator))
          memorylist.push(secondValue)
        } else {
          const tempmemory = memorylist
          memorylist = []
          memorylist.push(return_whole_number(aggregate_memory(tempmemory)))
          memorylist.push(return_corresponding_symbol(operator))
          memorylist.push(secondValue)
        }
        document.getElementById("calculator-memory").innerHTML = memorylist.join(' ');
        
        
        const calcValue = calculate(firstValue, operator, secondValue)
        display.textContent = calcValue
      
        // Update calculated value as firstValue
        calculator.dataset.firstValue = calcValue
        
        
        
  
      } else {
        // If there are no calculations, set displayedNum as the firstValue
        calculator.dataset.firstValue = displayedNum
      }
      
      key.classList.add('is-depressed')
      calculator.dataset.previousKeyType = 'operator'
      calculator.dataset.operator = action
      
      } else if (action === 'decimal') {
          if (!displayedNum.includes('.')) {
            display.textContent = displayedNum + '.'
          } else if (
            previousKeyType === 'operator' ||
            previousKeyType === 'calculate'
          ) {
            display.textContent = '0.'
          }
        
          calculator.dataset.previousKeyType = 'decimal'
          
        } else if (action === 'percent') {
          const tot = displayedNum.length
          const totless = displayedNum.length - 1
          
          if (!displayedNum.includes('.')) {
            if (displayedNum > 2) {

              display.textContent = displayedNum.substring(0, tot - 2) + '.' + displayedNum.substring(tot - 2, tot) 
            } else {
            display.textContent = '.' + displayedNum
            }
          } else if (
            previousKeyType === 'operator' ||
            previousKeyType === 'calculate'
          ) {
            display.textContent = '.0'
          }
        
          calculator.dataset.previousKeyType = 'decimal'
        }  else if (action === 'calculate') {
    const  firstValue = calculator.dataset.firstValue
    const  operator = calculator.dataset.operator
    const  secondValue = displayedNum
    
    if (firstValue) {
    if (previousKeyType === 'calculate') {
        firstValue = displayedNum
        secondValue = calculator.dataset.modValue
        
        
    }

    if (!memorylist[0]){
          memorylist.push(firstValue)
          memorylist.push(return_corresponding_symbol(operator))
          memorylist.push(secondValue)
        } else {
          const tempmemory = memorylist
          memorylist = []
          memorylist.push(return_whole_number(aggregate_memory(tempmemory)))
          memorylist.push(return_corresponding_symbol(operator))
          memorylist.push(secondValue)
        }
        document.getElementById("calculator-memory").innerHTML = memorylist.join(' ');
        
        
    display.textContent = calculate(firstValue, operator, secondValue)
  }

// Set modValue attribute
  calculator.dataset.modValue = secondValue
  calculator.dataset.previousKeyType = 'calculate'
  }

}
 
})