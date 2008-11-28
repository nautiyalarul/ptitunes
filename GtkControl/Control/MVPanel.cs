// MVPanel.cs
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
using GtkControl.Control;

namespace GtkControl
{
	
	
	public partial class MVPanel : Gtk.Bin
	{
		private Widget currCtrl = null;
		private Widget currClone = null;
		private int origX = 0;
		private int origY = 0;
		private int pointX = 0;
		private int pointY = 0;
		private bool isDragged = false;
		
		public MVPanel()
		{
			this.Build();
		}
		
		//Set the controls to be redrawn
		public void RefreshChildren()
		{
			this.fixed1.QueueDraw();
		}
		
		//Add a movable control to the panel
		public void AddMovingObject(string name,string caption, int x, int y)
		{
			//Prevent the object to be displayed outside the panel
			if (x<0)
			{
				x = 0;
			}
			
			if (y<0)
			{
				y = 0;
			}
			
			//Create the box where the custom object is rendered
			EventBox ev = GetMovingBox(name,caption);
			//Add the events to control the movement of the box
			ev.ButtonPressEvent+=new ButtonPressEventHandler(OnButtonPressed);
			ev.ButtonReleaseEvent+=new ButtonReleaseEventHandler(OnButtonReleased);
			
			//Add the control to the panel
			this.fixed1.Put(ev,x,y);
			this.ShowAll();
		}
		
		//Create the event box for the custom control
		private EventBox GetMovingBox(string name, string caption)
		{ 
			MVObject ctrl = new MVObject(name,caption);
			EventBox rev = new EventBox();
			rev.Name = name;
			rev.Add(ctrl);
			Console.WriteLine("Creating new moving object"+rev.Name);
			return rev;
		}
		
		//Create a clone of the selected object that will be shown until the destination of the control is reached
		private Widget CloneCurrCtrl()
		{
			Widget re = null;
			
			if (this.currCtrl!=null)
			{
				if (currCtrl is EventBox)
				{
					re = GetMovingBox((currCtrl as EventBox).Name+"Clone", ((currCtrl as EventBox).Child as MVObject).Caption);
				}
			}
			if (re==null)
			{
				//This should not really happen but that would prevent an exception
				re = GetMovingBox("Unknown","Unknown");
			}
			return re;
		}
		
		//Render the clone of the selected object at the intermediate position
		private void MoveClone(ref Widget wdg, object eventX,object eventY)
		{
			if (wdg == null)
			{
				wdg = CloneCurrCtrl();
				this.fixed1.Add(wdg);		
				this.ShowAll();
			}
			MoveControl(wdg,eventX,eventY,true);
		}
		
		//Move a control to the specified event location
		private void MoveControl(Widget wdg, object eventX,object eventY, bool isClone)
		{
			int destX = origX+System.Convert.ToInt32(eventX)+origX-pointX;
			int destY = origY+System.Convert.ToInt32(eventY)+origY-pointY;
			if (destX<0)
			{
				destX = 0;
			}
			if (destY<0)
			{
				destY = 0;
			}			
			this.fixed1.Move(wdg,destX,destY);
			if (!isClone)
			{
				Console.WriteLine("MovingBox KeyReleased:"+destX.ToString()+"-"+destY.ToString());
			}
			this.fixed1.QueueDraw();	
		}
		
		//Mouse click on the controls of the panel  
		protected void OnButtonPressed(object sender, ButtonPressEventArgs a)
		{		
			//Right click
			if (a.Event.Button==3)
			{
				if (sender is EventBox)
				{
					((sender as EventBox).Child as MVObject).ShowMenu();
				}	
			}
			//Left click
			else if (a.Event.Button==1)
			{
				//Double-click
				if (a.Event.Type==Gdk.EventType.TwoButtonPress)
				{
					if (sender is EventBox)
					{
						//Calling the edit method of the control
						((sender as EventBox).Child as MVObject).Edit();
					}	
				}
				else
				{
					//Setup the origin of the move
					isDragged = true;
					currCtrl = sender as Widget;
					currCtrl.TranslateCoordinates(this.fixed1,0,0,out origX, out origY);
					fixed1.GetPointer(out pointX,out pointY);
					Console.WriteLine("MovingBox KeyPressed");
					Console.WriteLine("Pointer:"+pointX.ToString()+"-"+pointY.ToString());
					Console.WriteLine("Origin:"+origX.ToString()+"-"+origY.ToString());
				}
			}
		}
	
		protected void OnButtonReleased(object sender, ButtonReleaseEventArgs a)
		{
			//Final destination of the control
			if (a.Event.Button==1)
			{
				MoveControl(currCtrl, a.Event.X,a.Event.Y,false);
				isDragged = false;
				currCtrl = null;
				if (currClone!=null)
				{
					this.fixed1.Remove(currClone);
					Console.WriteLine("Deleting moving object"+currClone.Name);
					currClone.Destroy();
					currClone = null;
				}
			}
		}

		//Called whenever a control is moved
		protected virtual void OnFixed1MotionNotifyEvent (object o, Gtk.MotionNotifyEventArgs args)
		{
			
			if (isDragged)
			{
				//Render of a clone at the desired location
				if (currCtrl!=null)
				{
					MoveClone(ref currClone, args.Event.X,args.Event.Y);
				}
			}
		}
	}	
}
