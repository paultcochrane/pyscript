# talk style for PyScript, following the Rico contributed design of prosper
# $Id$

HOME = os.path.expandvars("$HOME")
stylesDir = HOME + "/.pyscript/styles/"

# set the background colour of the slides
self.bg = Color('white')

# set the foreground and background colour of the title text of the talk
self.title_fg = Color('black')
self.title_bg = Color('black')

# set the talk title's text style
self.title_textstyle = r"\bf\sf"

# set the text style for the text of who is giving the talk
self.speaker_textstyle = r"\sf"

# set the colour and text style of the address of the speaker of the talk
self.address_fg = Color('black')
self.address_textstyle = r"\sf"

# set the colour and text style of the authors of the talk (not necessarily
# the speaker of the talk)
self.authors_fg = Color('black')
self.authors_textstyle = r"\sf"

# set the colour and text style of the title of the *slide*
self.slide_title_fg = Color('black')
self.slide_title_textstyle = r"\sf"
self.slide_title_scale = 5

# set the colour, scale, textstyle, bullet and indent type for a level 1 heading
self.headings_fgs[1] = Color('black')
self.headings_scales[1] = 3
self.headings_textstyle[1] = r"\sf"
self.headings_bullets[1] = Epsf(file=stylesDir+"rico_bullet1.ps").scale(0.5,0.5)
self.headings_indent[1] = 0

# set the colour, scale, textstyle, bullet and indent type for a level 2 heading
self.headings_fgs[2] = Color('black')
self.headings_scales[2] = 2.5
self.headings_textstyle[2] = r"\sf"
self.headings_bullets[2] = Epsf(file=stylesDir+"rico_bullet2.ps").scale(0.4,0.4)
self.headings_indent[2] = 0.5

# set the colour, scale, textstyle, bullet and indent type for a level 3 heading
self.headings_fgs[3] = Color('black')
self.headings_scales[3] = 2.2
self.headings_textstyle[3] = r"\sf"
self.headings_bullets[3] = Epsf(file=stylesDir+"rico_bullet3.ps").scale(0.3,0.3)
self.headings_indent[3] = 1 

# set the colour, scale, textstyle, bullet and indent type for an equation heading
self.headings_fgs['equation'] = Color('black')
self.headings_scales['equation'] = 2.5
self.headings_textstyle['equation'] = r""
self.headings_bullets['equation'] = Rectangle(height=1, fg=self.bg, bg=self.bg)
self.headings_indent['equation'] = 2 

# set the colour, textstyle and scale for placed text
self.text_scale = 3.0
self.text_fg = Color('black')
self.text_textstyle = r"\sf"

# set the colours of the waitbar
self.waitbar_fg = Color('#bcfe04')
self.waitbar_bg = Color('black')

# define the custom background pattern generating function
self.make_background_func = """
back = Group()
back.append(Rectangle(sw=self.area.sw,
		width=self.area.width,
		height=self.area.height,
		fg=None,
		bg=talk.bg,
		)
	    )

bar = Epsf(file="%s", width=20)
bar.ne = self.area.ne+P(-1,-2)
back.append(bar)

corner_nw = Epsf(file="%s", width=1)
corner_nw.rotate(90, p=corner_nw.c)
corner_nw.c = self.area.nw+P(1,-1.8)
back.append(corner_nw)

corner_sw = Epsf(file="%s", width=1)
corner_sw.rotate(0, p=corner_sw.c)
corner_sw.c = self.area.sw+P(1,1.8)
back.append(corner_sw)

corner_ne = Epsf(file="%s", width=1)
corner_ne.rotate(180, p=corner_ne.c)
corner_ne.c = self.area.ne+P(-1,-1.8)
back.append(corner_ne)

corner_se = Epsf(file="%s", width=1)
corner_se.rotate(-90, p=corner_se.c)
corner_se.c = self.area.se+P(-1,1.8)
back.append(corner_se)
""" % (stylesDir+"barre-rico.ps", stylesDir+"angleHG.ps", 
	stylesDir+"angleHG.ps", stylesDir+"angleHG.ps",
	stylesDir+"angleHG.ps")

