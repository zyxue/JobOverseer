import StringIO
from xml.dom.minidom import Document

def main():
    with open("clusters.xml", 'w') as opf:
	doc = Document()
    	write_clusters(doc, opf)
    with open("users.xml", 'w') as opf:
	doc = Document()
	write_users(doc, opf)
	opf.close

def write_clusters(doc, outputfile):
    DATA = [
	# [[name, cores, statcmd], ...]
	["scinet", 8, "/usr/local/bin/showq --format=xml",
	 ["gpc-f101n084", "gpc-f102n084", "gpc-f103n084", "gpc-f104n084", "gpc-logindm01"]
	 ],

	["mp2", 24, "/opt/torque/bin/qstat -x",
	 ["ip13", "cp2540", "ip14"]
	 ],

	["guillimin", 12, "/opt/moab/bin/showq --format=xml",
	 ["lg-1r14-n01", "lg-1r14-n02", "lg-1r14-n03", "lg-1r14-n04", "lg-1r14-n05"]
	 ],

	["lattice", 8, "/usr/local/moab/bin/showq --format=xml",
	 ["lattice"]
	 ],

	["orca", 24, "/opt/sharcnet/moab/6.1.3/bin/showq --format=xml",
	 ["orc-login1", "orc-login2"]
	 ],

	["nestor", 8, "/opt/bin/qstat -x",
	 ["litai05.westgrid.ca"]
	 ],

        ["colosse", 8, "/opt/moab/bin/showq --format=xml",
         ["colosse1", "colosse2"]
         ]

	]

    tags = ["clustername", "cores-per-node", "statcmd"]

    # First basenode
    clusters = doc.createElement("clusters")
    doc.appendChild(clusters)

    for k, datum in enumerate(DATA):
	cluster = doc.createElement("cluster")
	clusters.appendChild(cluster)
	cluster.setAttribute('id', "cluster{0:02d}".format(k+1))

	# handling all properties other than hostnames
	for tag, d in zip(tags, datum[:-1]):
	    elm = doc.createElement(tag)
	    cluster.appendChild(elm)
	    text = doc.createTextNode(str(d))
	    elm.appendChild(text)
    
	# start handling hostnames from here
	hostnames = doc.createElement("hostnames")
	cluster.appendChild(hostnames)
	for hostname in datum[-1]:	
	    hn = doc.createElement("hn") # hn: hostname
	    hostnames.appendChild(hn)
	    text = doc.createTextNode(hostname)
	    hn.appendChild(text)
    
    print doc.toprettyxml(indent="  ")
    doc.writexml(outputfile)			# this is not pretty

def write_users(doc, outputfile):
    DATA = '''
        Zhuyi Xue           = xuezhuyi zyxue zhuyxue12
        ChrisI Ing          = ingchris cing ceing
        Loan Huynh          = huynhloa lhuynh
        John Holyoake       = holyoake holyoake
        ChrisN Neale        = nealechr cneale
        Sarah Rauscher      = rauscher srausche
        David Caplan        = dacaplan
        Grace Li            = ligrace1 grace
        Nilu Chakrabarti    = chakraba nilu nchakrab12
        Kethika Kulleperuma = kulleper kethika7 kkullepe12 kkullepe
        Aditi Ramesh        = rameshad aditi
        ChrisM Madill       = cmadill
        jnachman?(scinet)   = jnachman
        Ana Nikolia         = nikolia
        Regis Pomes         = pomes
        efadda?(orca)       = efadda
        sbaud?(orca)        = sbaud
    '''
    tags = ["username", "realname"]
    
    users = doc.createElement("users")
    doc.appendChild(users)

    data = StringIO.StringIO(DATA)
    k = 0
    for line in data:
	if line.strip():
	    user = doc.createElement("user")
	    users.appendChild(user)
	    user.setAttribute('id', "user{0:02d}".format(k+1))
	    
	    sl = [i.strip() for i in line.split("=")]
	    ssl = sl[1].split()
	    for username in ssl:
		un = doc.createElement(tags[0]) # un: username
		user.appendChild(un)
		text = doc.createTextNode(username)
		un.appendChild(text)
	    
		rn = doc.createElement(tags[1]) # rn: realname
		user.appendChild(rn)
		text = doc.createTextNode(sl[0])
		rn.appendChild(text)
	    k += 1
    
    print doc.toprettyxml(indent="  ")
    doc.writexml(outputfile)			# this is not pretty

if __name__ == "__main__":
    main()


    # Worked hard to format the following data like that, though not useful at
    # the moment, prefer just to leave it there

# DATA = [
#     "[Zhuyi Xue", ["xuezhuyi", "zyxue", "zhuyxue12"]],
#     "[ChrisI Ing", "["ingchris", "cing", "ceing"]],
#     "[Loan Huynh", "["huynhloa", "lhuynh"]],
#     "[John Holyoake", "["holyoake", "holyoake"]],
#     "[ChrisN Neale", "["nealechr", "cneale"]],
#     "[Sarah Rauscher", "["rauscher", "srausche"]],
#     "[David Caplan", "["dacaplan"]],
#     "[Grace Li", "["ligrace1", "grace"]],
#     "[Nilu Chakrabarti", "["chakraba", "nilu", "nchakrab12"]],
#     "[Kethika Kulleperuma", "["kulleper", "kethika7", "kkullepe12", "kkullepe"]],
#     "[Aditi Ramesh", "["rameshad", "aditi"]],
#     "[ChrisM Madill", "["cmadill"]],
#     "[jnachman?(scinet)", "["jnachman"]],
#     "[Ana Nikolia", "["nikolia"]],
#     "[Regis Pomes", "["pomes"]],
#     "[efadda?(orca)", "["efadda"]],
#     "[sbaud?(orca)", "["sbaud"]],


