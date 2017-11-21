:title: Astrophysics Research Python Programming
:slug: astrophysics-scientific-python-programming
:date: 2017-08-20 09:01:44
:athuors: Arnon Sela, Daniel Sela
:tags: Science, Automation, Academia, Astrophysics, Research, Python, IDL

-----------------------
The Productive Research
-----------------------

Introduction
============

Recently I helped a group of astrophysicists convert a set of IDL programs to Python. This set was to classify stars by analyzing ROTSE-I and ROTSE-III data. In this insert I would share the experience of moving IDL code to python. The insert is only attempt to cover interesting aspects that we encountered. At the same time, it serves as an encouragement to perform such migration. Python is a powerful tool. As a software architect I recognize the readability of Python programs, the vast libraries that one can tap on, and the large community that continues enrich its capabilities (scientific, WEB, network, you name it, its there).

In fact, Python is being used for Data Analytics and Machine Learning; just google it around you will see many courses in the realm. So basically, with scipy_, numpy_, pandas_, matplotlib_, and more, one can accomplish everything done with IDL and more.

.. _numpy: http://www.numpy.org/
.. _scipy: https://docs.scipy.org/doc/numpy/index.html
.. _pandas: http://pandas.pydata.org/
.. _matplotlib: https://matplotlib.org/

From IDL to Python
==================

IDL is a "scientific programming language used across disciplines to extract meaningful visualizations from complex numerical data. With IDL you can interpret your data, expedite discoveries, and deliver powerful applications to market." It uses plenty vector and matrix computation. So we will have a lot of that with numpy computing techniques.

Loading FITS and MATCH
----------------------

The first we have to be able to read the ROTSE-I and ROTSE-III data files.  There were three types of files.

    1. .dat: MATCH structure
    #. .datc: compressed MATCH structure
    #. .fit: FITS structure

Luckily, all these structures are readable natively by python packages. The following code insert shows how to read MATCH and FITS structured files.

    .. code-block:: python

        from scipy.io import readsav
        import pyfits

        def read_fits_file(file, fits_index=1):
            try:
                hdus = pyfits.open(file, memmap=True)
                hdus_ext=hdus[fits_index]
                data=hdus_ext.data
            except Exception as e:
                raise Exception("cannot read fits data from file: %s" % (file,)) from e
            return data


        def read_match_file(file, *args, **kwargs):
            try: data=readsav(file)['match']
            except Exception as e:
                raise Exception("cannot read match data from file: %s" % (file,)) from e
            return data

The above code uses two packages `scipy.io`__ and pyfits_, which provides the actual loading of the structures. Note that *readsav* reads both .dat and .datc files.

.. _pyfits: https://pythonhosted.org/pyfits/

.. _scipy_io: https://docs.scipy.org/doc/scipy-0.19.1/reference/io.html

__ scipy_io_

The type of the resulting data is of type `numpy.recarry`__.  Elements of recarray can be accessed via name either by the '.' or '[]' notation.

.. _recarray: https://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html
__ recarray__

It is easy to have a general purpose reader by having a routing function as follows:

    .. code-block:: python

        def read_data_file(file, fits_index=1, tmpdir='/tmp'):
            if not os.path.isfile(file):
                raise Exception("file not found: %s" % (file,))

            file_ext=file.rpartition('.')[2]
            if file_ext=='fit':
                data=read_fits_file(file, fits_index)
            else: # assume MATCH
                data=read_match_file(file)
            return data

Obviously, this is good only if the next processing steps takes into account differences between the two structures. For example, MATCH structure have a STAT field that is not part of FITS structute.

    .. code-block:: python

        try: stat=data.field('STAT')[0]
        except: stat=None # assume not a MATCH file


Where statement
---------------

IDL programs take advantage of IDL's *where_* statement. It will look something like follows:

.. _where: https://www.harrisgeospatial.com/docs/WHERE.html

    .. code-block:: python

        select_indexes = where(data.flags[*,ptr] gt -1 and $
            check_flags(ref_vflag, data.flags[*,ptr], type='STYPE') eq 0)

The above statement is pretty loaded in functionality.  In essence, the expected result are indexes into the vector data.values[*,k] that adheres to two conditions: the need to be greater than -1; and the result for the function *check_value* to be zero.

    .. code-block:: python

        import numpy as np

        # assum data is a MATCH or FITS data structure
        # and that check_flag function is defined for ref_flag and
        flags=data.field('FLAGS')[0]
        check_flags_v=np.vectorize(lambda flag: check_flag(ref_flag, flag) ==0)
        cond=np.logical_and.reduce( (flags[ptr,:] > -1,
                                     check_flags_v(flags[ptr,:]), ), )
        select_indexes=np.where(cond); select_indexes=select_indexes[0]

To match IDL with Python, we are using four distinct numpy functions.
    1. *vectorize* transforms a vector by applying a function on its elements.
    #. *logical_and* and *reduce*: applys logical test to vector element transforming it to boolean vector.
    #. *where*: return indices of those element set to True.

An important note is that IDL matrix indices are in opposite order to that of numpy.

From here on we will assume *np* stands for numpy imported as np.

Just to clarify, numpy performs operation on arrays. For example, assuming *merr* and *msys* are arrays of the same size, the following will produce a new array which each element is the square root of the squared sum of related elements. Obviously, a more sophisticated computation can be deployed.

    .. code-block:: python

        np.sqrt(merr**2.0 + msys**2.0)

Hierarchical record array initialization
----------------------------------------

IDL's *create_struct_* is being used to create records with fields accessible by name.
It's parallel in numpy realm is recarray_.

.. _create_struct: https://www.harrisgeospatial.com/docs/create_struct.html

.. _recarray: https://docs.scipy.org/doc/numpy/reference/generated/numpy.recarray.html

The following code set shows how to create recarray structure with default values. Starting with the definition of the records' fields, field_map.  it is built as a list of tuple, each describe a name a field, a type, and a default value.

    .. code-block:: python

        field_map=[
            ('state', int, -1),
            ('distance', np.float32, -1.0),
            ('posangle', np.float32, -1.0),
            ('error', np.float32, -1.0),
            ('phot', np.float32, -1.0),
            ('photerror', np.float32, -1.0),]

Next, base on the above mapping, *create_structured_vector* would create the records' data type and a vector[size] with elements of the desired data type.

    .. code-block:: python

        def create_structured_vector(size, field_map, copy=False):
            dts=list()
            for name, type_, _ in field_map:
                dts.append( (name, type_,) )
            dtype = np.dtype(dts)

            values=[tuple([value if not copy else np.copy(value)
                           for _, _, value in field_map]) for _ in range(size)]
            array=np.rec.array(values, dtype=dtype)

            return array, dtype

The copy option of *create_structured_vector*, if set, tells it to copy the default values. This is useful in case the default value is a structure by itself.

Note that the function returns a tuple of the generated array and the created type. This is useful in case further association of this data type is required.

This method could be extended to handle any array shape, not just vectors.

Plotting
--------

IDL's plot capability can be achieved using *matplotlib* and *pandas's* dataframe.plot. These tools are rich with features and easy to use.

The original IDL code we were porting was built creating postscript documents. Using matplotlib we switched to PDF.

Here is an example how to print few drawing per page. We start with importing and setting matpolotlib for PDF plotting.

    .. code-block:: python

        import matplotlib
        matplotlib.use('PDF')
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_pdf import PdfPages

Next, we define subplot on a page organized by 3 rows of 2 figure each.
Assuming that data is a list of tuples (title, values), we

    .. code-block:: python

        pdf=PdfPages('pdffile.pdf')

        for i in range(len(data)):

            if i%6 == 0: # first in a page
                fig, axarr = plt.subplots(3, 2, figsize=(11, 8.5))

            # data = [(title, x-values, y-values), ...]
            k=i%6;
            fig=axarr[int(k/2), k-int(k/2)*2]
            title, x_values, y_values = data[i]
            fig.set_title(title, fontsize=11)
            fig.plot(x_values, y_values, '+')

            if i%6 == 5: # last in a page
                fig.tight_layout(pad=0.4, w_pad=0.5, h_pad=1.0)
                pdf.savefig()
                plt.close()

        pdf.close()

Moment
------

*moment* is an IDL function that provides in a single call 4 statistical calculations. *moment* returns a four-element vector containing the mean, variance, skewness, and kurtosis of the input vector.

Similar functionality can be accomplish using numpy and scipy.

.. code-block:: python

    from scipy import stats

    def moment(value_vec)
        mean=np.mean(value_vec)
        sdev=np.sqrt(np.var(value_vec))
        skew=stats.skew(value_vec)
        vkurt=stats.kurtosis(value_vec)

        return mean, sdev, skew, vkurt

scipy's *stats_* has many other shortcut computations that are worth a while to look at. In reality, it is rare that one needs all four computational elements. Therefore, it is better to engage with the specific functions as needed instead of using moment().

.. _stats: https://docs.scipy.org/doc/scipy-0.19.1/reference/stats.html


Store and Recover
=================

It can be quite annoying to debug the last step in a multi-steps analytic were each step is a computation taking a long time. Well, once you pass the first step, debugging each consequent step can be annoying.

What you want to do is to keep state of the multi-step process such that data would be stored after each completed step. That will allow you to jump into the step being debugged immediately.

A simple mechanism to do that is to store the dataset at the end of each step. Before the step starts, the program can check if a result is stored for that step. If so, it recovers and skips the step.

There needs to be a few flags for a program that does that. One --recoverable to enable the mechanism to store datasets. --recover to enable loading previously stored recovery datasets. Also, --recdir to set location for recovery datasets (obviously naming is merely a suggestion).

    .. code-block:: python

        step_1_var_rec=None; step_var_1=None
        if recoverable:
            step_1_var_rec=Recovery('step_var_1', match_file)
            if recover:
                step_var_1=step_1_var_rec.load()

    .. code-block:: python

        if step_1_var_rec and step_var_1 is not None:
            step_1_var_rec.store(step_var_1)

The code for *Recovery* shown here is a bit elaborated. Its sophistication arises from that it automates recovery based on time comparison of a source file (*assoc_path*) and the recoverable storage. This is done in the load function.

    .. code-block:: python

        class Recovery(object):
            def __init__(self, name, assoc_path, location=None):
                self.assoc_path=assoc_path
                self.name=name
                self.obj_file=self.get_obj_file(location)

            def get_obj_file(self, location=None):
                result=self.assoc_path+'.%s'%self.name
                if location:
                    name=os.path.basename(result)
                    result=os.path.join(location, name)
                return result

            def load(self,):
                obj=None
                if self.obj_file:
                    if os.path.isfile(self.obj_file):
                        obj_file_m_time = os.path.getmtime(self.obj_file)
                        assoc_path_m_time=0
                        if os.path.isfile(self.assoc_path) or os.path.isdir(self.assoc_path):
                            assoc_path_m_time = os.path.getmtime(self.assoc_path)
                        if assoc_path_m_time > 0 and obj_file_m_time >= assoc_path_m_time:
                            # not a new file, read goodobj from file
                            print("Recovering %s from %s" %(self.name, self.obj_file))
                            with open(self.obj_file, 'rb') as f:
                                obj=pickle.load(f)
                return obj

            def store(self, obj):
                print("Storing %s into %s" %(self.name, self.obj_file))
                with open(self.obj_file, 'wb') as f:
                    pickle.dump(obj, f)

Interesting astrophysics packages
=================================

Through the work, we ran into two Python packages for astronomy.

Astropy_: "A Community Python Library for Astronomy."

PyAstronomy_: "A collection of astronomy related packages."

.. _Astropy: http://www.astropy.org/
.. _PyAstronomy: http://www.hs.uni-hamburg.de/DE/Ins/Per/Czesla/PyA/PyA/index.html

These packages contain plenty of easy to use functionality. However, be cautious when using in high volume processing. Not all computations may meet your need for performance. For example, we had to rewrite IDL's *SIXTY_* instead of using an already made solution in these libraries. Only a scaled down version meet our performance needs.

.. _SIXTY: https://www.harrisgeospatial.com/docs/sixty.html

References
==========

`IDL to Numeric/numarray Mapping`__

.. _idl_numeric_numarray: http://www.johnny-lin.com/cdat_tips/tips_array/idl2num.html
__ idl_numeric_numarray_

`NumPy for IDL users`__

.. _NumPy_for_IDL: http://mathesaurus.sourceforge.net/idl-numpy.html
__ NumPy_for_IDL_

`Ten Little IDL programs in Python`__

.. _ten_little_idl: http://blog.rtwilson.com/ten-little-idl-programs-in-python/
__ ten_little_idl_

`The IDL Astronomy User's Library`__

.. _nasa_idl_lib: https://idlastro.gsfc.nasa.gov/
__ nasa_idl_lib_

`HARRIS's IDL`__

.. _harris: http://www.harrisgeospatial.com/ProductsandTechnology/Software/IDL.aspx
__ harris_

Give us your feedback: support@acrisel.com
