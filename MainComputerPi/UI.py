import urwid

# custom widget to show 3d box outline
class LineBox(urwid.WidgetDecoration, urwid.WidgetWrap):

    def __init__(self, original_widget, title="",
                 title_align="center", title_attr=None,
                 tlcorner=u'┌', tline=u'─', lline=u'│',
                 trcorner=u'┐', blcorner=u'└', rline=u'│',
                 bline=u'─', brcorner=u'┘', light_attr=None, dark_attr=None):
        """
        Draw a line around original_widget.
        Use 'title' to set an initial title text with will be centered
        on top of the box.
        Use `title_attr` to apply a specific attribute to the title text.
        Use `title_align` to align the title to the 'left', 'right', or 'center'.
        The default is 'center'.
        You can also override the widgets used for the lines/corners:
            tline: top line
            bline: bottom line
            lline: left line
            rline: right line
            tlcorner: top left corner
            trcorner: top right corner
            blcorner: bottom left corner
            brcorner: bottom right corner
            light_attr: palette entry for light colors
            dark_attr: palette entry for dark colors
        If empty string is specified for one of the lines/corners, then no
        character will be output there.  This allows for seamless use of
        adjoining LineBoxes.
        """

        if tline:
            if light_attr:
                tline = urwid.AttrMap(urwid.Divider(tline), light_attr)
            else:
                tline = urwid.Divider(tline)
        if bline:
            if dark_attr:
                bline = urwid.AttrMap(urwid.Divider(bline), dark_attr)
            else:
                bline = urwid.Divider(bline)
        if lline:
            if light_attr:
                lline = urwid.AttrMap(urwid.SolidFill(lline), light_attr)
            else:
                lline = urwid.SolidFill(lline)
        if rline:
            if dark_attr:
                rline = urwid.AttrMap(urwid.SolidFill(rline), dark_attr)
            else:
                rline = urwid.SolidFill(rline)
        if light_attr:
            tlcorner, blcorner = urwid.AttrMap(urwid.Text(tlcorner), light_attr), urwid.AttrMap(urwid.Text(blcorner), light_attr)
        else:
            tlcorner, blcorner = urwid.Text(tlcorner), urwid.Text(blcorner)
        if dark_attr:
            trcorner, brcorner = urwid.AttrMap(urwid.Text(trcorner), dark_attr), urwid.AttrMap(urwid.Text(brcorner), dark_attr)
        else:
            trcorner, brcorner = urwid.Text(trcorner), urwid.Text(brcorner)

        if not tline and title:
            raise ValueError('Cannot have a title when tline is empty string')

        if title_attr:
            self.title_widget = urwid.Text((title_attr, self.format_title(title)))
        else:
            self.title_widget = urwid.Text(self.format_title(title))

        if tline:
            if title_align not in ('left', 'center', 'right'):
                raise ValueError('title_align must be one of "left", "right", or "center"')
            if title_align == 'left':
                tline_widgets = [('flow', self.title_widget), tline]
            else:
                tline_widgets = [tline, ('flow', self.title_widget)]
                if title_align == 'center':
                    tline_widgets.append(tline)
            self.tline_widget = urwid.Columns(tline_widgets)
            top = urwid.Columns([
                ('fixed', 1, tlcorner),
                self.tline_widget,
                ('fixed', 1, trcorner)
            ])

        else:
            self.tline_widget = None
            top = None

        middle_widgets = []
        if lline:
            middle_widgets.append(('fixed', 1, lline))
        else:
            # Note: We need to define a fixed first widget (even if it's 0 width) so that the other
            # widgets have something to anchor onto
            middle_widgets.append(('fixed', 0, urwid.SolidFill(u"")))
        middle_widgets.append(original_widget)
        focus_col = len(middle_widgets) - 1
        if rline:
            middle_widgets.append(('fixed', 1, rline))

        middle = urwid.Columns(middle_widgets,
                box_columns=[0, 2], focus_column=focus_col)

        if bline:
            bottom = urwid.Columns([
                ('fixed', 1, blcorner), bline, ('fixed', 1, brcorner)
            ])
        else:
            bottom = None

        pile_widgets = []
        if top:
            pile_widgets.append(('flow', top))
        pile_widgets.append(middle)
        focus_pos = len(pile_widgets) - 1
        if bottom:
            pile_widgets.append(('flow', bottom))
        pile = urwid.Pile(pile_widgets, focus_item=focus_pos)

        urwid.WidgetDecoration.__init__(self, original_widget)
        urwid.WidgetWrap.__init__(self, pile)

    def format_title(self, text):
        if len(text) > 0:
            return " %s " % text
        else:
            return ""