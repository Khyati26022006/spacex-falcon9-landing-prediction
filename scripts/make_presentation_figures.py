import pandas as pd, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge, Polygon, Rectangle
BLUE='#0B49CB'; GREEN='#1E9E5A'; RED='#D64545'; NAVY='#0A2A66'; GREY='#5B6577'
plt.rcParams.update({'font.family':'DejaVu Sans','axes.edgecolor':'#C8D0DE','axes.labelcolor':NAVY,'xtick.color':GREY,'ytick.color':GREY,'axes.spines.top':False,'axes.spines.right':False,'font.size':12})
d=pd.read_csv('spacex.csv'); d.columns=[c.strip() for c in d.columns]
d['Launch_Site']=d.Launch_Site.str.strip(); d['Orbit']=d.Orbit.str.strip()
d['class']=d.Landing_Outcome.str.strip().str.startswith('Success').astype(int)
d['FN']=np.arange(1,len(d)+1)
dd=pd.read_csv('dash.csv')
def cat_scatter(df,x,ycol,xl,yl,fn,order=None,xlim=None,figsize=(8.2,4.4)):
    fig,ax=plt.subplots(figsize=figsize,dpi=200)
    order=order or sorted(df[ycol].unique())
    yi={k:i for i,k in enumerate(order)}
    for c,col,lab in [(0,RED,'Failure'),(1,GREEN,'Success')]:
        s=df[df['class']==c]
        ax.scatter(s[x],[yi[v] for v in s[ycol]]+np.random.RandomState(1).uniform(-.18,.18,len(s)),c=col,s=46,alpha=.85,edgecolor='white',linewidth=.6,label=lab)
    ax.set_yticks(range(len(order))); ax.set_yticklabels(order); ax.set_xlabel(xl); ax.set_ylabel(yl)
    ax.grid(axis='x',color='#E6EAF2'); ax.set_axisbelow(True)
    if xlim: ax.set_xlim(*xlim)
    ax.legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,1.12),ncol=2)
    fig.tight_layout(); fig.savefig(fn,transparent=False,facecolor='white'); plt.close(fig)
sites=['CCAFS LC-40','CCAFS SLC-40','KSC LC-39A','VAFB SLC-4E']
cat_scatter(dd.rename(columns={'Flight Number':'FN','Launch Site':'Site','Payload Mass (kg)':'PL'}),'FN','Site','Flight number','Launch site','figs/fn_site.png',order=sites)
cat_scatter(dd.rename(columns={'Flight Number':'FN','Launch Site':'Site','Payload Mass (kg)':'PL'}),'PL','Site','Payload mass (kg)','Launch site','figs/pl_site.png',order=sites)
orbs=['LEO','LEO (ISS)','Polar LEO','SSO','MEO','GTO','HEO','Sub-orbital']
o=d[d.Orbit.isin(orbs)]
cat_scatter(o,'FN','Orbit','Flight number (chronological)','Orbit','figs/fn_orbit.png',order=orbs)
cat_scatter(o,'PAYLOAD_MASS__KG_','Orbit','Payload mass (kg)','Orbit','figs/pl_orbit.png',order=orbs)
# insight: booster era chart handled natively. Dash scatter payload vs outcome
def dash_scatter(lo,hi,fn):
    fig,ax=plt.subplots(figsize=(6.4,3.55),dpi=200)
    s=dd[(dd['Payload Mass (kg)']>=lo)&(dd['Payload Mass (kg)']<=hi)]
    cols={'v1.0':'#9AA5B8','v1.1':'#F2A100','FT':BLUE,'B4':GREEN,'B5':RED}
    for k,c in cols.items():
        t=s[s['Booster Version Category']==k]
        ax.scatter(t['Payload Mass (kg)'],t['class'],c=c,s=70,edgecolor='white',linewidth=.7,label=k,alpha=.9)
    ax.set_xlim(-300,10300); ax.set_ylim(-.25,1.25); ax.set_yticks([0,1]); ax.set_xlabel('Payload mass (kg)'); ax.set_ylabel('Class (1 = landed)')
    ax.grid(color='#E6EAF2'); ax.set_axisbelow(True); ax.legend(frameon=False,ncol=5,loc='upper center',bbox_to_anchor=(.5,1.17),fontsize=12,handletextpad=.2,columnspacing=1.0)
    fig.tight_layout(); fig.savefig(fn,facecolor='white'); plt.close(fig)
dash_scatter(0,10000,'figs/dash_all.png'); dash_scatter(2000,5500,'figs/dash_mid.png')
# Folium-style schematics
def ocean(ax,coast,side,xl,yl):
    ax.set_facecolor('#DCE9FB'); ax.set_xlim(*xl); ax.set_ylim(*yl)
    xs,ys=zip(*coast)
    edge=xl[0] if side=='W' else xl[1]
    land=list(coast)+([(xl[0],yl[1]),(xl[0],yl[0])] if side=='E' else [(xl[1],yl[1]),(xl[1],yl[0])])
    # land is to the west for Florida (E coast) and east for California
    ax.add_patch(Polygon(land,closed=True,fc='#EEF1E6',ec='#9AA5B8',lw=1.2,zorder=1))
    ax.set_xticks([]); ax.set_yticks([])
    for s in ax.spines.values(): s.set_color('#C8D0DE')
fl=[(-80.0,26.4),(-80.05,27.2),(-80.35,27.9),(-80.55,28.4),(-80.6,28.8),(-80.85,29.2),(-81.1,29.9),(-81.3,30.5)]
fl_land=[(-84,26.4)]+fl+[(-84,30.5)]
ca=[(-120.5,34.2),(-120.6,34.45),(-120.65,34.58),(-120.58,34.75),(-120.62,35.0)]
sitexy={'CCAFS LC-40':(-80.577356,28.562302),'CCAFS SLC-40':(-80.576820,28.563197),'KSC LC-39A':(-80.646895,28.573255),'VAFB SLC-4E':(-120.610746,34.632834)}
stat={'CCAFS LC-40':(7,26),'CCAFS SLC-40':(3,7),'KSC LC-39A':(10,13),'VAFB SLC-4E':(4,10)}
# 1: global-ish: two panels
fig,axs=plt.subplots(1,2,figsize=(10,4.6),dpi=200,gridspec_kw={'width_ratios':[1,1]})
a=axs[0]; a.set_facecolor('#DCE9FB'); a.set_xlim(-83,-78.5); a.set_ylim(26.5,30.2)
a.add_patch(Polygon(fl_land,closed=True,fc='#EEF1E6',ec='#9AA5B8',lw=1.2)); a.set_xticks([]);a.set_yticks([])
a.text(-82.8,30.0,'Florida, USA',color=NAVY,fontsize=13,weight='bold',va='top')
for s in ['KSC LC-39A','CCAFS LC-40']:
    x,y=sitexy[s]; a.add_patch(plt.Circle((x,y),.18,fc=BLUE,alpha=.22,ec=BLUE,lw=1.2)); a.scatter([x],[y],c=BLUE,s=70,zorder=5)
a.annotate('KSC LC-39A',(-80.646895,28.573255),xytext=(-83.0,28.95),fontsize=11,color=NAVY,arrowprops=dict(arrowstyle='-',color=GREY),weight='bold')
a.annotate('CCAFS LC-40 / SLC-40',(-80.577,28.563),xytext=(-82.9,27.9),fontsize=11,color=NAVY,arrowprops=dict(arrowstyle='-',color=GREY),weight='bold')
b=axs[1]; b.set_facecolor('#DCE9FB'); b.set_xlim(-123,-118.6); b.set_ylim(33.2,36.0)
b.add_patch(Polygon(ca+[(-118.6,35.0),(-118.6,34.2)],closed=True,fc='#EEF1E6',ec='#9AA5B8',lw=1.2)); b.set_xticks([]);b.set_yticks([])
b.text(-122.8,35.85,'California, USA',color=NAVY,fontsize=13,weight='bold',va='top')
x,y=sitexy['VAFB SLC-4E']; b.add_patch(plt.Circle((x,y),.2,fc=BLUE,alpha=.22,ec=BLUE,lw=1.2)); b.scatter([x],[y],c=BLUE,s=70,zorder=5)
b.annotate('VAFB SLC-4E',(x,y),xytext=(-122.8,34.2),fontsize=11,color=NAVY,arrowprops=dict(arrowstyle='-',color=GREY),weight='bold')
for ax_ in axs:
    for s in ax_.spines.values(): s.set_color('#C8D0DE')
    ax_.spines['top'].set_visible(True); ax_.spines['right'].set_visible(True)
fig.tight_layout(); fig.savefig('figs/map1.png',facecolor='white'); plt.close(fig)
# 2: outcome markers
fig,ax=plt.subplots(figsize=(10,4.6),dpi=200)
ax.set_facecolor('#DCE9FB'); ax.set_xlim(-81.35,-79.9); ax.set_ylim(28.2,28.95)
ax.add_patch(Polygon([(-82,28.0)]+[(-80.55,28.4),(-80.6,28.8),(-80.85,29.2)][:0]+[(-80.55,28.2),(-80.55,28.45),(-80.6,28.8),(-80.7,29.0),(-82,29.0)],closed=True,fc='#EEF1E6',ec='#9AA5B8',lw=1.2))
ax.set_xticks([]);ax.set_yticks([])
def glyph(ax,x,y,s,f,r=.07):
    ax.add_patch(Wedge((x,y),r,90,90+360*s/f,fc=GREEN,ec='white',lw=1,zorder=5))
    ax.add_patch(Wedge((x,y),r,90+360*s/f,450,fc=RED,ec='white',lw=1,zorder=5))
pos={'KSC LC-39A':(-80.95,28.75,'KSC LC-39A\n10 of 13 landed (77%)',-81.3),'CCAFS LC-40':(-80.58,28.52,'CCAFS LC-40\n7 of 26 landed (27%)',-80.35),'CCAFS SLC-40':(-80.58,28.36,'CCAFS SLC-40\n3 of 7 landed (43%)',-80.35)}
for k,(x,y,lab,tx) in pos.items():
    s,f=stat[k]; glyph(ax,x,y,s,f)
    ax.annotate(lab,(x,y),xytext=(tx,y+(.0 if k!='CCAFS SLC-40' else -.02)),fontsize=11,color=NAVY,weight='bold',va='center',arrowprops=dict(arrowstyle='-',color=GREY),ha='left')
ax.text(-81.3,28.9,'Launch outcomes by site',fontsize=13,color=NAVY,weight='bold',va='top'); ax.text(-81.3,28.82,'(markers offset for readability)',fontsize=9.5,color=GREY,va='top')
ax.scatter([-81.3],[28.28],c=GREEN,s=60); ax.text(-81.25,28.28,'success',va='center',fontsize=10.5,color=NAVY)
ax.scatter([-81.08],[28.28],c=RED,s=60); ax.text(-81.03,28.28,'failure',va='center',fontsize=10.5,color=NAVY)
for s_ in ax.spines.values(): s_.set_color('#C8D0DE')
ax.spines['top'].set_visible(True); ax.spines['right'].set_visible(True)
fig.tight_layout(); fig.savefig('figs/map2.png',facecolor='white'); plt.close(fig)
# 3: proximity (schematic)
fig,ax=plt.subplots(figsize=(10,4.6),dpi=200); ax.set_facecolor('#EEF1E6'); ax.set_xlim(0,10); ax.set_ylim(0,5); ax.set_xticks([]);ax.set_yticks([])
ax.add_patch(Rectangle((7.2,0),2.8,5,fc='#DCE9FB',ec='none')); ax.plot([7.2,7.2],[0,5],c='#9AA5B8',lw=1.5)
ax.text(8.6,4.6,'Atlantic Ocean',ha='center',color=NAVY,fontsize=12,style='italic')
ax.plot([0,7],[1.9,1.9],c=GREY,lw=3,ls=(0,(6,3))); ax.text(.2,1.55,'Railway',color=GREY,fontsize=11)
ax.plot([0,7],[3.0,3.0],c='#F2A100',lw=4); ax.text(.2,3.15,'Highway',color='#B57A00',fontsize=11)
sx,sy=6.0,2.45
for (tx,ty,lab) in [(7.2,2.45,'Coastline  ~0.9 km'),(6.0,1.9,'Railway  ~1.3 km'),(6.0,3.0,'Highway  ~0.6 km')]:
    ax.plot([sx,tx],[sy,ty],c=BLUE,lw=1.8)
ax.text(7.35,2.5,'Coastline\n~0.9 km',fontsize=11,color=NAVY,weight='bold',va='center')
ax.text(5.1,1.45,'~1.3 km',fontsize=11,color=NAVY,weight='bold'); ax.text(5.05,3.3,'~0.6 km',fontsize=11,color=NAVY,weight='bold')
ax.scatter([sx],[sy],c=BLUE,s=140,zorder=6,edgecolor='white'); ax.text(sx-.15,sy,'CCAFS SLC-40',ha='right',va='center',fontsize=11.5,color=NAVY,weight='bold')
ax.annotate('Nearest city (Melbourne, FL)\n~51 km south-west',(.3,.4),xytext=(.3,.4),fontsize=11,color=NAVY,weight='bold')
ax.text(.2,4.6,'Schematic - not to scale',fontsize=10,color=GREY)
for s_ in ax.spines.values(): s_.set_color('#C8D0DE')
fig.tight_layout(); fig.savefig('figs/map3.png',facecolor='white'); plt.close(fig)
print('ok')
