// MVObject.cs
// 
// Copyright (C) 2008 Olivier Lecointre - Cadexis
//
// This program is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program.  If not, see <http://www.gnu.org/licenses/>.
//

using System;
using Gtk;

namespace GtkControl.Control
{
	
	public class MVObject : Gtk.DrawingArea 
	{
		Pango.Layout titleLayout;
		Gtk.DrawingArea da;
		string parentName = "";
		string caption = "";
		Gtk.Menu popup = null;
		string body = "";
		int width = 0;
		
		public MVObject(string pName, string cap)
		{

			popup = new Gtk.Menu();
			
			Gtk.MenuItem text1 = new MenuItem("Test1");
			text1.Activated+=new EventHandler(Menu1Clicked);
			Gtk.MenuItem text2 = new MenuItem("Test2");
			text2.Activated+=new EventHandler(Menu2Clicked);
			
			popup.Add(text1);			
			popup.Add(text2);
			
			parentName = pName;
			caption = cap;
			width = caption.Length*8+10;
			
			this.Name = parentName+"MVObject";
			
			this.SetSizeRequest(width,40);
			
			titleLayout = GetLayout(caption);
		}
		
		public void ShowMenu()
		{
			if (popup!=null)
			{
				popup.Popup();
				popup.ShowAll();
			}
		}
		
		public void Edit()
		{
			body="Edit";
			this.QueueDraw();
		}
		
		public string Caption
		{
			get
			{
				return caption;
			}
		}
		
		public void Redraw()
		{
			Console.WriteLine("Redrawing");
			this.QueueDraw();
		}
		
		private Pango.Layout GetLayout(string text)
		{
			Pango.Layout layout = new Pango.Layout(this.PangoContext);
			layout.FontDescription = Pango.FontDescription.FromString("monospace 8");
			layout.SetMarkup("<span color=\"black\">" + text + "</span>");
			return layout;
		}
		
		protected void Menu1Clicked(object sender, EventArgs args)
		{
			Console.WriteLine("Test");
			body = "Test1";
			this.QueueDraw();
		}
		
		protected void Menu2Clicked(object sender, EventArgs args)
		{
			Console.WriteLine("Test");
			body = "Test2";
			this.QueueDraw();
		}
		
		protected override bool OnExposeEvent (Gdk.EventExpose args)
		{	
			Gdk.Window win = args.Window;
			Gdk.Rectangle area = args.Area;
			
			
			win.DrawRectangle(Style.DarkGC(StateType.Normal), true, area);
			win.DrawRectangle(Style.BlackGC,false,area);
			win.DrawRectangle(Style.MidGC(StateType.Normal),true,0,15,1000,1000);
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

