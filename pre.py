"""
Test program for pre-processing schedule
"""
import arrow

base = arrow.now()

def process(raw):
    """
    Line by line processing of syllabus file.  Each line that needs
    processing is preceded by 'head: ' for some string 'head'.  Lines
    may be continued if they don't contain ':'.  
    """	
    field = None
    entry = { }
    cooked = [ ] 
    for line in raw:
        line = line.rstrip()
        if len(line) == 0:
            continue
        parts = line.split(':')
        if len(parts) == 1 and field:
            entry[field] = entry[field] + line
            continue
        if len(parts) == 2: 
            field = parts[0]
            content = parts[1]
        else:
            raise ValueError("Trouble with line: '{}'\n".format(line) + 
                "Split into |{}|".format("|".join(parts)))

        if field == "begin":
            try:
                content = content[2:]
                base = arrow.get(content,"MM/DD/YYYY")
            except:
                raise ValueError("Unable to parse date {}".format(content))

        elif field == "week":
            if entry:
                cooked.append(entry)
                entry = { }
            entry['topic'] = ""
            entry['project'] = ""
            #content = int(content)
            #base = base.replace(week=+content)
            #base = base.replace(week=+int(content))
            #entry['week'] = base.replace(week=+1).format("MM/DD/YYYY")
            content2 = int(content)-1
            entry['week'] = base.replace(weeks=+content2).format("MM/DD/YYYY")
            now= arrow.utcnow().format('MM/DD/YYYY')
            weekBegin = base.replace(weeks=+content2).format("MM/DD/YYYY")
            weekEnd = base.replace(weeks=+content2+1).format("MM/DD/YYYY")
            if (now >= weekBegin and now < weekEnd):
                thisWeek=True
            else:
                thisWeek = False
            entry['thisweek1'] = thisWeek
        elif field == 'topic' or field == 'project':
            entry[field] = content

        else:
            raise ValueError("Syntax error in line: {}".format(line))

    return cooked


def main():
    f = open("static/schedule.txt")
    parsed = process(f)
    print(parsed)

if __name__ == "__main__":
    main()

    
    
            
    
