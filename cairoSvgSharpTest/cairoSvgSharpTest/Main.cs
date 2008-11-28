// Main.cs created with MonoDevelop
// User: jonathan at 2:13 AM 11/28/2008
//
// To change standard headers go to Edit->Preferences->Coding->Standard Headers
//
using System;
using Gtk;
using Cairo;
using Rsvg;
using System.Runtime.InteropServices; //for DLL import
using Accessibility;
using System.Data;

namespace RoadSVG {
   class RoadSVG: Gtk.Window {
		
	private Gtk.DrawingArea da;

	public RoadSVG(): base("RoadSVG") {
	   this.DeleteEvent += Quit;
	   this.da = new Gtk.DrawingArea();
			this.da.ExposeEvent += Draw;
	   this.Add(da);
	   this.da.Show();
	}
      public static void Main(string[] args) {
         Application.Init();
         RoadSVG w = new RoadSVG();
         w.Show();
         Application.Run();
      }
		
		void Draw(object o, Gtk.ExposeEventArgs e) {
			MyRsvg.Handle s = new MyRsvg.Handle("/home/jonathan/Prods/prog/PT1/clickWheelUnTouchedState.svg");
    Cairo.Context context = Gdk.CairoHelper.Create(this.da.GdkWindow);
 s.RenderOn(context);
    /*context.MoveTo(10,10);
    context.LineTo(100,10);
    context.LineTo(100,100);
    context.LineTo(10,100);
    context.LineTo(10,100);
    context.ClosePath();
                 
    context.Color = new Cairo.Color(0,0,0);
    context.FillPreserve();
    context.Color = new Cairo.Color(1,0,0);
    context.Stroke();*/
			
			
 }
      

      void Quit(object sender, DeleteEventArgs a){
         Application.Quit();
         a.RetVal = true;
      }
   }
}

namespace MyRsvg {
    class Handle: Rsvg.Handle {
	
//missing methods from .Net (for now) abstracted from C dll: 
		[DllImport("rsvg-2")]
internal static extern IntPtr rsvg_handle_new_from_file(IntPtr file_name, out IntPtr error);
		
		[DllImport("rsvg-2")]
internal static extern void rsvg_handle_render_cairo(IntPtr handle, IntPtr cairoContext);

[DllImport("rsvg-2")]
internal static extern void rsvg_handle_render_cairo_sub(IntPtr handle, IntPtr cairoContext, string id);
		
	protected static IntPtr NewFromFile(string fileName) {
   IntPtr error = IntPtr.Zero;
   IntPtr nativeFileName = GLib.Marshaller.StringToPtrGStrdup(fileName);
   IntPtr handlePtr = rsvg_handle_new_from_file(nativeFileName, out error);
   GLib.Marshaller.Free(nativeFileName);

   if(IntPtr.Zero != error){
      throw new GLib.GException(error);
   }

   return handlePtr;
}	
		
		public void RenderOn(Cairo.Context context) {
   rsvg_handle_render_cairo(this.Raw, context.Handle);
}

public void RenderOn(Cairo.Context context, string id) {
   rsvg_handle_render_cairo_sub(this.Raw, context.Handle, id);
}
		
		[StructLayout(LayoutKind.Sequential)]
public class RsvgDimensionData {
   public int width;
   public int heigh;
   public double em;
   public double ex;
}

[DllImport("rsvg-2")]
internal static extern void rsvg_handle_get_dimensions(IntPtr handle,
                                                       [Out, MarshalAs(UnmanagedType.LPStruct)]
                                                       out RsvgDimensionData dimension_data);

RsvgDimensionData GetDimensions() {
   Console.WriteLine("GetDimensions()");
   RsvgDimensionData dd;
   rsvg_handle_get_dimensions(this.Raw, out dd);
   Console.WriteLine("return dd");
   return dd;
}

		
public int Width {
   get {
      return this.Pixbuf.Width;
   }
}

public int Height {
   get {
      return this.Pixbuf.Height;
   }
}


public Handle(string fileName): base(MyRsvg.Handle.NewFromFile(fileName)) {
   // Do nothing. Everything was done by NewFormFile and the base class.
}


public Handle(System.IntPtr data): base(data) {
   // Just reimplement the constructor.
}

public Handle(): base() {
   // Just reimplement the constructor.
}

		static protected byte[] StreamToArray(System.IO.Stream st) {
   if(st.Length > int.MaxValue) {
      // TODO: raise exception or something.
      return null;
   } else {
      // TODO: not all streams have a length and can be read completely, do something about it, like raising an exception.
      System.IO.StreamReader str = new System.IO.StreamReader(st);
      System.Text.UTF8Encoding encoder = new System.Text.UTF8Encoding();
      return encoder.GetBytes(str.ReadToEnd());
   }
}
		
    } //Handle class
 }//namespace