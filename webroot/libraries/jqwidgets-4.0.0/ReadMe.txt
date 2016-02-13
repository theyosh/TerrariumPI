1. The SDK files are located in the jqwidgets directory
 
 In general you need to use files from this directory only.

 Files list & description:

  Files required in all projects using the SDK:

  jqxcore.js: Core jQWidgets framework

  Stylesheet files. Include at least one stylesheet Theme file and the images folder:

  styles/jqx.base.css: Stylesheet for the base Theme. The jqx.base.css file should be always included in your project.
  
  styles/jqx.android.css: Stylesheet for the Android Theme
  styles/jqx.arctic.css: Stylesheet for the Arctic Theme
  styles/jqx.web.css: Stylesheet for the Web Theme
  styles/jqx.black.css: Stylesheet for the Black Theme
  styles/jqx.blackberry.css: Stylesheet for the Blackberry Theme
  styles/jqx.bootstrap.css: Stylesheet for the Bootstrap Theme
  styles/jqx.classic.css: Stylesheet for the Classic Theme
  styles/jqx.darkblue.css: Stylesheet for the DarkBlue Theme
  styles/jqx.energyblue.css: Stylesheet for the EnergyBlue Theme
  styles/jqx.fresh.css: Stylesheet for the Fresh Theme
  styles/jqx.highcontrast.css: Stylesheet for the High Contrast Theme
  styles/jqx.metro.css: Stylesheet for the Metro Theme
  styles/jqx.metrodark.css: Stylesheet for the Metro Dark Theme
  styles/jqx.mobile.css: Stylesheet for the Mobile Theme
  styles/jqx.office.css: Stylesheet for the Office Theme
  styles/jqx.orange.css: Stylesheet for the Orange Theme
  styles/jqx.shinyblack.css: Stylesheet for the ShinyBlack Theme
  styles/jqx.summer.css: Stylesheet for the Summer Theme
  styles/jqx.windowsphone.css: Stylesheet for the Windows Phone Theme
  styles/jqx.ui-darkness.css: Stylesheet for the UI Darkness Theme
  styles/jqx.ui-lightness.css: Stylesheet for the UI Lightness Theme
  styles/jqx.ui-le-frog.css: Stylesheet for the UI Le Frog Theme
  styles/jqx.ui-overcast.css: Stylesheet for the UI Overcast Theme
  styles/jqx.ui-redmond.css: Stylesheet for the UI Redmond Theme
  styles/jqx.ui-smoothness.css: Stylesheet for the UI Smoothness Theme
  styles/jqx.ui-start.css: Stylesheet for the UI Start Theme
  styles/jqx.ui-sunny.css: Stylesheet for the UI Sunny Theme

  styles/images: contains images referenced in the stylesheet files
  
  Files for individual widgets and plug-ins. Include depending on project needs:
	
  jqxangular.js: AngularJS integration plug-in
  jqxbuttons.js: Button, RepeatButton, SubmitButton & ToggleButton widgets
  jqxbulletchart.js: BulletChart widget
  jqxbuttongroup.js: Button group widget
  jqxcalendar.js: Calendar widget
  jqxcombobox.js: ComboBox widget
  jqxcomplexinput.js: Complex Numbers TextBox widget
  jqxchart.core.js: Chart widget's Core
  jqxchart.rangeselector.js: Chart Range Selector
  jqxchart.api.js: Chart API
  jqxchart.annotations.js: Chart's annotations
  jqxchart.waterfall.js: Waterfall Chart
  jqxcheckbox.js: CheckBox widget
  jqxdate.js: DateTime plug-in
  jqxdata.js: Data Source plug-in
  jqxdata.export.js: Data Export plug-in
  jqxdatetimeinput.js: DateTimeInput widget
  jqxcolorpicker.js: Color Picker widget
  jqxdatatable.js: DataTable widget
  jqxdocking.js: Docking widget
  jqxdropdownbutton.js: DropDown Button widget
  jqxdragdrop.js: DragDrop plug-in
  jqxdraw.js: Draw Plugin.
  jqxdockpanel.js: DockPanel widget
  jqxdockinglayout.js: Docking Layout widget
  jqxdropdownlist.js: DropDownList widget
  jqxeditor.js: Editor widget
  jqxexpander.js: Expander widget
  jqxfileupload.js: FileUpload widget
  jqxformattedinput.js: Binary, Octal, Hex TextBox widget
  jqxgrid.js: Grid widget
  jqxgrid.sort.js: Grid Sort plug-in
  jqxgrid.filter.js: Grid Filter plug-in
  jqxgrid.grouping.js: Grid Grouping plug-in
  jqxgrid.selection.js: Grid Selection plug-in
  jqxgrid.columnsresize.js: Grid Columns Resize plug-in
  jqxgrid.columnsreorder.js: Grid Columns Reorder plug-in
  jqxgrid.pager.js: Grid Pager plug-in
  jqxgrid.edit.js: Grid Editing plug-in
  jqxgrid.storage.js: Grid Save/Load state plug-in
  jqxgrid.aggregates.js: Grid Aggregates plug-in
  jqxgauge.js: Radial and Linear Gauge widget
  jqxinput.js: TextBox widget
  jqxknockout.js: Knockout integration plug-in
  jqxknob.js: Knob widget
  jqxkanban.js: Kanban widget
  jqxlayout.js: Layout widget
  jqxlistbox.js: ListBox widget
  jqxloader.js: Loader widget
  jqxmaskedinput.js: Masked TextBox widget
  jqxmenu.js: Menu widget
  jqxnavigationbar.js: NavigationBar widget
  jqxnavbar.js: NavBar widget
  jqxnotification.js: Notification widget
  jqxnumberinput.js: NumberInput TextBox widget
  jqxpanel.js: Panel widget
  jqxpopover.js: Popover widget
  jqxprogressbar.js: ProgressBar widget
  jqxpasswordinput.js: Password input widget
  jqxrating.js: Rating widget
  jqxradiobutton.js: RadioButton widget
  jqxrangeselector.js: RangeSelector widget
  jqxresponse.js: Response plug-in
  jqxribbon.js: Ribbon widget
  jqxresponsivepanel.js: Responsive Panel widget
  jqxswitchbutton.js: Switch Button widget
  jqxscrollbar.js: ScrollBar widget
  jqxscrollview.js: ScrollView widget
  jqxsplitter.js: Splitter widget
  jqxslider.js: Slider widget
  jqxscheduler.js: Scheduler widget
  jqxscheduler.api.js: Scheduler API plugin
  jqxsortable.js: Sortable plugin
  jqxtabs.js: Tabs widget
  jqxtree.js: Tree widget
  jqxtagcloud.js: Tagcloud widget
  jqxtreemap.js: TreeMap widget
  jqxtreegrid.js: TreeGrid widget
  jqxtoolbar.js: Toolbar widget
  jqxtooltip.js: ToolTip widget
  jqxvalidator.js: Validation plug-in
  jqxwindow.js: Window widget

  File for all widgets and plug-ins:

  jqx-all.js

2.Examples

  The index.htm file starts the demo/examples browser
  Individual widget examples are located in the /demos directory
  The mobile examples are located in the /mobiledemos directory
  The php & mysql integration demos are located in the /phpdemos and demos/php directories. 
  All php integration samples use and require the Northwind Database(/phpdemos/Northwind.MySQL5.sql).  
  Any examples that use Ajax need to be on a Web Server in order to work correctly. 

3.Documentation

  Browse the documentation and examples through the index.htm file
  Individual documentation files are located in the /documentation directory
   
4.Other files

  The /scripts, /images, /styles folders contain the jquery library and
  other files used by the demo only.

5.License & Purchase

   For more information regarding the licensing, please visit: http://www.jqwidgets.com/license

