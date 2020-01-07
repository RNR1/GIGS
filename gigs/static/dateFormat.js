let dates = document.querySelectorAll('time')
let months = document.querySelectorAll(".month")
let days = document.querySelectorAll(".day")
let nums = document.querySelectorAll(".day-num")
let start = document.querySelectorAll(".time")
let times = document.querySelectorAll(".time")
for (let i in dates) {
    let month = moment(dates[i].dateTime).format("MMMM")
    let day = moment(dates[i].dateTime).format("dddd")
    let num = moment(dates[i].dateTime).format("D")
    let time = moment(start[i]).format("HH:mm")
    months[i].textContent = month
    days[i].textContent = day
    nums[i].textContent = num
    times[i].textContent = time 
    }