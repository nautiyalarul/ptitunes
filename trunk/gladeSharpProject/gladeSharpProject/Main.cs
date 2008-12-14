// Main.cs created with MonoDevelop
// User: jonathan at 11:12 PM 11/27/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//
using System;
using Gtk;
using Glade;

public class GladeApp
{
	public static void Main (string[] args)
	{
		new GladeApp (args);
	}
	
	static void on_mainTabLeftViewportFixed_expose_event(object obj, Gtk.ExposeEventArgs args)
	{
		Gtk.Fixed fix = (Gtk.Fixed) obj;
		//Gtk.TreeView tv1 = Glade.XML("treeview1","");

		//tv1.Model = ls;
		
		Gtk.Image clickWheelBgImage = new Gtk.Image("/home/jonathan/Prods/prog/PT1/188188.png");
		clickWheelBgImage.SetSizeRequest(188,188);
		clickWheelBgImage.Show();
		fix.Add(clickWheelBgImage);
	}
	
	void on_mainTabEventsTreeView_show(object obj, EventArgs args)
	{
		Gtk.ListStore ls = new Gtk.ListStore(typeof(Gdk.Pixbuf),typeof(string));
	    //Gdk.Pixbuf pb = new Gdk.Pixbuf("/home/jonathan/Prods/prog/PT1/188188.png");
		//ls.AppendValues(pb,"bonjour");
		//GtK.CellRendererPixbuf crpb = Gtk.CellRendererPixbuf();
		
		Gtk.TreeView tv = new Gtk.TreeView(ls);
		
		
	}

	public GladeApp (string[] args) 
	{
		Application.Init ();

		Glade.XML gxml = new Glade.XML (null, "gui.glade", "window1", null);
		gxml.Autoconnect (this);
		Application.Run ();
	}

	// Connect the Signals defined in Glade
	private void OnWindowDeleteEvent (object sender, DeleteEventArgs a) 
	{
		Application.Quit ();
		a.RetVal = true;
	}
}

