import pandas as pd
import numpy as np
from dateutil.rrule import weekday

# 生成示例日期数据
dates = pd.date_range(start='2023-01-01', end='2024-07-01')

# 生成示例值数据
values = np.random.randint(1, 100, size=len(dates))

# 创建数据框
data = pd.DataFrame({
    'value': values,
    'date': dates,
})

date = data["date"]
value = data["value"]

#%%
import matplotlib.pyplot as plt
fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(date, value);
plt.show()


#%%
import matplotlib.dates as mdates
fig, ax = plt.subplots(figsize=(8, 6))

half_year_locator = mdates.MonthLocator(interval=6)
ax.xaxis.set_major_locator(half_year_locator) # Locator for major axis only.

ax.plot(date, value)

plt.show()

#%%
fig, ax = plt.subplots(figsize=(8, 6))

half_year_locator = mdates.MonthLocator(interval=6)
year_month_formatter = mdates.DateFormatter("%Y-%m") # four digits for year, two for month

ax.xaxis.set_major_locator(half_year_locator)  # 刻度长度是
ax.xaxis.set_major_formatter(year_month_formatter) # 刻度显示格式

ax.plot(date, value)

plt.show()

#%% Add minor tick marks
fig, ax = plt.subplots(figsize=(8, 6))

monthly_locator = mdates.MonthLocator()
ax.xaxis.set_major_locator(half_year_locator)
ax.xaxis.set_minor_locator(monthly_locator)
ax.xaxis.set_major_formatter(year_month_formatter)
ax.plot(date, value)

fig.autofmt_xdate()

plt.show()

#%%
month_year_formatter = mdates.DateFormatter('%b, %Y') # The "," is intentional.

fig, ax = plt.subplots(figsize=(8, 8))

monthly_locator = mdates.MonthLocator()
ax.xaxis.set_major_locator(half_year_locator)
ax.xaxis.set_minor_locator(monthly_locator)
ax.xaxis.set_major_formatter(month_year_formatter)
sec = ax.secondary_xaxis(location=-0.075)
sec.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=1))
sec.xaxis.set_major_formatter(mdates.DateFormatter('%A'))
ax.plot(date, value)
fig.autofmt_xdate()

plt.show()



#%%
fig, ax = plt.subplots()

# 主轴按月显示日期
monthly_locator = mdates.MonthLocator()
monthly_formatter = mdates.DateFormatter('%Y-%m')
ax.xaxis.set_major_locator(monthly_locator)
ax.xaxis.set_major_formatter(monthly_formatter)

# 副轴按星期几缩写显示
sec = ax.secondary_xaxis(location=-0.075)
weekday_locator = mdates.WeekdayLocator()
weekday_formatter = mdates.DateFormatter('%a')
sec.xaxis.set_major_locator(weekday_locator)
sec.xaxis.set_major_formatter(weekday_formatter)
fig.autofmt_xdate()
ax.plot(data['date'], data['value'])
for label in sec.xaxis.get_ticklabels():
    label.set_rotation(45)  # 设置副轴刻度标签旋转 45 度
fig.autofmt_xdate()
plt.show()


#%%

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# 生成示例日期数据
dates = pd.date_range(start='2023-01-01', end='2023-01-07')

# 生成示例值数据
values = np.random.randint(1, 100, size=len(dates))

# 创建数据框
data = pd.DataFrame({
    'date': dates,
    'value': values
})

fig, ax = plt.subplots()

# 主轴按具体日期显示
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))

# 副轴按星期几缩写显示
sec = ax.secondary_xaxis(location=-0.075)
weekday_locator = mdates.WeekdayLocator()
weekday_formatter = mdates.DateFormatter('%a')
sec.xaxis.set_major_locator(weekday_locator)
sec.xaxis.set_major_formatter(weekday_formatter)

for label in sec.xaxis.get_ticklabels():
    label.set_rotation(45)  # 设置副轴刻度标签旋转 45 度

ax.plot(data['date'], data['value'])
fig.autofmt_xdate()

plt.show()

#%%
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np

# 生成示例日期数据
dates = pd.date_range(start='2023-01-01', end='2023-01-07')

# 生成示例值数据
values = np.random.randint(1, 100, size=len(dates))

# 创建数据框
data = pd.DataFrame({
    'date': dates,
    'value': values
})

fig, ax = plt.subplots()



fig.subplots_adjust(left=0.2, right=0.8, bottom=0.4, top=0.8)  # 您可以根据需要调整这些值

# 主轴按具体日期显示
ax.xaxis.set_major_locator(mdates.DayLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))


sec = ax.secondary_xaxis(location=-0.15)
weekday_locator = mdates.WeekdayLocator(byweekday=[0,1,2,3,4,5,6])
weekday_formatter = mdates.DateFormatter('%a')
sec.xaxis.set_major_locator(weekday_locator)
sec.xaxis.set_major_formatter(weekday_formatter)
sec.xaxis.set_tick_params(which='major', length=0)
sec.spines['bottom'].set_visible(False)

ax.plot(data['date'], data['value'])

for label in sec.xaxis.get_ticklabels():
    label.set_rotation(45)
    label.set_horizontalalignment('right')  # 调整副轴标签水平对齐方式为右对齐plt.show()
    label.set_color('red')
    label.set_fontsize(8)

for label in ax.xaxis.get_ticklabels():
    label.set_rotation(45)
    label.set_horizontalalignment('right')  # 调整主轴标签水平对齐方式为右对齐


plt.show()