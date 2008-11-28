// hop.cs created with MonoDevelop
// User: jonathan at 8:33 AM 11/28/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//

using System;
using Gtk;

namespace GtkControl.Control
{
    
    public class MVObject : Gtk.DrawingArea 
    {
        
        public MVObject(string pName, string cap)
        {
                  //...
        }
                
        public void Redraw()
        {
            this.QueueDraw();
        }

               private Pango.Layout GetLayout(string text)
        {
            Pango.Layout layout = new Pango.Layout(this.PangoContext);
            layout.FontDescription = Pango.FontDescription.FromString("monospace 8");
            layout.SetMarkup("<span color=\"black\">" + text + "</span>");
            return layout;
        }
        
        protected override bool OnExposeEvent (Gdk.EventExpose args)
        {    
            Gdk.Window win = args.Window;
            Gdk.Rectangle area = args.Area;
                
            win.DrawRectangle(Style.DarkGC(StateType.Normal), true, area);
            win.DrawRectangle(Style.MidGC(StateType.Normal),true,0,15,1000,1000);
            win.DrawRectangle(Style.BlackGC,false,area);
            win.DrawLine(Style.BlackGC,0,15,1000,15);            
            win.DrawLayout(Style.BlackGC,2,2,titleLayout);

            if (!string.IsNullOrEmpty(body))
            {
                win.DrawLayout(Style.BlackGC,2,17,GetLayout(body));
            }
            return true;
        } 
    }
}