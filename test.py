from generate_content import scrape

with open("example_html.html","wb") as f:
    html = scrape("https://skillbee.com/")
    f.write(html)

with open("example_description.txt","w") as f:
    description = """
What draws me to Skillbee isn't just its impressive statistics or its extensive list of job offerings across the UAE and Gulf region. It's the palpable impact the platform has on people's lives.

When I explore Skillbee, I see more than just a job search app; I see a community where job seekers and employers converge to create meaningful connections. Skillbee isn't just about finding any job; it's about finding the right job, quickly and efficiently.

What truly resonates with me is the trust that Skillbee has built within the Gulf talent market. The testimonials speak volumes. Hearing from individuals like Khwaja Hussain, Zulfikar Ahmed, and Imtiyaz Ahmed, who found their perfect jobs through Skillbee, underscores the platform's effectiveness and reliability.

It's not just about the numbers for me; it's about the stories behind them. Stories of individuals who found their career paths through Skillbee, stories of timely calls and direct job placements, stories of empowerment and opportunity.

Skillbee isn't merely a job search tool; it's a catalyst for change in people's lives. And that, above all else, is what truly interests me about the company. I'm drawn to the idea of being part of a team that's not just facilitating job searches but transforming lives and livelihoods in the process.


"""
    f.write(description)