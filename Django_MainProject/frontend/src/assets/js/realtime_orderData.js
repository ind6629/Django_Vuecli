function createLineBox(){
    //console.log(orders);
    datax = [];
    list_data = []
    orders.forEach(order => {
        datax.push(`${order.date}`);
        item = {};
        item['value'] = `${order.times}`;
        item['label'] = {show: true, formatter: `${order.category}` };
        list_data.push(item);
      });
    console.log('datax:',datax)
    console.log('list_data:',list_data)

    let chartDom = document.querySelector('.lineBox');
    let myChart = echarts.init(chartDom);
    let option;

    option = {
        xAxis: {
        type: 'category',
        data: datax,
        axisLabel: {
        interval: 0, // 强制显示所有标签
        rotate: 30,  // 标签旋转30度防止重叠
        formatter: function(value) {
        return value.split('-').slice(1).join('-'); // 简化为"月-日"格式
    ss}
  }
        },
        yAxis: { type: 'value' },
        series: [{
          data: list_data,
          type: 'line',
          label: {  // 默认配置
            show: true,
            position: 'top',
            color: '#333',
            fontSize: 12
          }
        }]
      };
    
    option && myChart.setOption(option);
    console.log('加载订单数据');
}

function createBarBox(){
let chartDom = document.querySelector('.barBox');
let myChart = echarts.init(chartDom);
let option;

dataDict = {}
orders.forEach(order => {
        category = order.category;
        times = order.times;
        if(category in dataDict)
            dataDict[category] += times;
        else{
            dataDict[category] = times;
        }
      });
dataX = [];
dataY = [];
for (let key in dataDict) {
    dataX.push(key);
    dataY.push(dataDict[key]);
}


option = {
  tooltip: {
    trigger: 'axis',
    axisPointer: {
      type: 'shadow'
    }
  },
  grid: {
    left: '3%',
    right: '4%',
    bottom: '3%',
    containLabel: true
  },
  xAxis: [
    {
      type: 'category',
      data: dataX,
      axisTick: {
        alignWithLabel: true
      }
    }
  ],
  yAxis: [
    {
      type: 'value'
    }
  ],
  series: [
    {
      name: 'Direct',
      type: 'bar',
      barWidth: '60%',
      data: dataY
    }
  ]
};

option && myChart.setOption(option);
}

function initBox(){
    createLineBox();
    createBarBox();
}
  
  
  
document.addEventListener('DOMContentLoaded', function() {
    initBox();
});