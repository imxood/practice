```
def writeRowContent(filename, rowToInsert, content, rowToDel = 0, totleToDel = 0):
    with open(filename, 'r+') as f:
        lines = f.readlines()
        while totleToDel > 0:
            lines.pop(rowToDel-1)
            totleToDel -= 1
        lines.insert(rowToInsert-1, content)
        f.seek(0, 0)
        f.truncate()
        f.writelines(lines)
        f.flush()
```
