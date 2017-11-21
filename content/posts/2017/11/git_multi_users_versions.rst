:title: Projects with Multiple Developers and Versions
:slug: manage-project-user-changes-and-versions
:date: 2017-11-15 20:47
:authors: Arnon Sela
:tags: git, version, multiple, develop, program, scope, project

--------------------------------------------------
git: Manage Developer Changes and Project Versions
--------------------------------------------------

Synopsis
========

There are many ways to use git to manages changes. This insert focus is the use of git in a development environment to handle changes of multiple versions done by various developers.

.. _`version tree`:

.. image:: /images/git_multi_users_versions/git_versions_and_branches.png
    :scale: 25%
    :align: right
    :alt: versions tree
    :class: image-process-large-photo

Mainstream development (next version) is always done in *main* branch. When next version is ready to be *freeze-d*, a branch is created with the version symbol. A tag with version name is also created to allow pull of specific version. Applying bug fix to a version under maintenance is done on the version branch. Once ready to be published, a proper subbranch is created.

A developer that works on a version branch (*v-tag*) would follow this procedure:
1. Pull changes into local and create a private branch to make changes.
2. Pull latest changes into local and merge them into private.
3. Merge private branch into local branch and push changes.

With this methodology, development of changes in multiple version by multiple developers.

Motivation
==========

Developers constantly apply changes to project code base. If they don't, they are not doing their job. These changes are either driven by new or change in requirements or by bug fix. Project management together with users and programmers agrees on phases and scope for their project. These phases and scope define project versions and releases.

It is common to have a development team supported multiple phases of a project at the same time. One phase is in production (or public release); bug fixes to issues reported by users are deployed here. Another phase is testing; this phase would be released next; fixes to issues reported by testers are deployed here. Yet another phase is developing the next phase that would be released to test.

It is also common to have much more than three phases being maintained at the same time. Fixes to issues in one phase also may be needed to be retrofitted into other phases.

Using git in our projects, we needed a simple methodology to have developers manage changes and versions.  This method, although expressed in git terms, can be used with any other version control system.

Introduction
============

This insert describes how to manage versions and development with git_. The management of version content (scope) is beyond the scope of this insert. 

To discuss code versions we have to invoke product life-cycle. Regardless to project methodology to manage life-cycle (e.g., agile), product life involves requirements, design, development, test, and run. Each of its parts is a world by itself. For example, the development team will have its version of tests. That test life-cycle itself may include unit-test, and integration-test, system-test. 

The development team creates and manages the code base of a project. It needs a way to manage the scope of changes as it relates to product life-cycle. The scope may include new features (e.g., the first version contains only new features), bug-fixes, or any combination of new or enhanced features and bug-fixes. That is where versions come to rescue. Product scope is mapped into versions. Every part of the life-cycle may have a different version of the product.

Obviously, life-cycle of large-scale software products is much more complicated then as described above. One reason is that large products are split into smaller functional projects that have their one life-cycle. The final product is a mash of those smaller projects bundled together in harmony (which is not simple to achieve as any conductor would testify). Another reason is the pressure from stakeholders (users and such) to push new features, enhancements, and fixes rapidly. 

If at all, this plays back into the need to have a good version management and development tools to apply it.

Version Management
==================

Version management is a combination of methodology and tools that in one end would define the scope of versions and on the other end would let programmers and administrator manage code. Figure `version tree`_ shows a simple example of how versions may be handled in git_. 

Software project initial phase is the simplest, at the beginning, there are only requirements. Programmers would work on *main* branch developing initial scope, the first version of the product. Once mature, the product moves to the next stage, test. At the same time of the product is being tested, programmers would have a new scope of requirements.

At that point, of delivery to test, there are two versions of the product being handled. Programmers continue to develop next version of the product. They also continue to maintain the version which was just delivered to test. Bugs found in test need to be fixed in both versions. New features would go into development version. 

Programmers will use a code management system to access to multiple versions of code. In our example, git_ is used. At the time of maturity, version administrator will freeze the code by tagging with a new version name (like v1.0 as in `version tree`_). 

The administrator will create a branch reflecting that tag. When programmers develop new features, main branch would be their friend. Checkin and checkout would be done to the main branch. When programmers work on bug fix to earlier versions, *checkout* and *checkin* to the appropriate version branch.


Administrator Perspective
=========================

A version administrator would use git_ to freeze version once mature for delivery. Freezing a version would be done with either branch or tag. We use *branch* in major and subversions. *Tag* is used to a critical fix that needs to be delivered in an immediate time-frame. 

There are other ways to manage versions with *branches* and *tags*. For example, a small project may start freezing code using *tags*. If a new fix needs to be pushed to an earlier version, only then, a branch would be created from the *tag* of that version.

1. Before creating branch *git checkout main* to make sure new branch is created from *main*. If a sub-version is created, *checkout version-name* to ensure the sub-branch is created from the right version.
2. *git checkout -b version-name* would create new branch of of existing *checkout* branch. 
3. or, *git tag -a version-name -m version-name* would create a tag reflecting the version and branch.
4. *git push origin version-name* will push the newly created version to a remote repository. 

Note, it is advisable for version administrator to create reports which will provide insight to versions and tags in repositories. Often enough a rogue *branch* or *tag* will find their way to the repository. To prevent confusion, periodical cleanup of unnecessary *branches* and tags would increase repository performance.

Programmer Perspective
======================

Programmers will need to be able to work on multiple versions in their sandbox. Often, they will need to retrofit fixes done on one branch into another. *git merge* cannot be used due to the potential need to selectively apply such changes.

A developer can create multiple footprints of the same remote repository into his environment and then *git checkout* different versions.  

On any particular change, programmers will want to work in isolation from the actual branch and then merge back their changes into the version. By this, if for some reason they want to discard work, they can do so by merely removing their branch.
 
A developer who works on a version branch (*version-name*) would follow this procedure:
1. *git pull* *version-name*
2. Create a local branch reflecting that branch, *v-work*.
3. Apply changes to *v-work* (add and commit). 

Meantime, other developers may apply changes. Therefore, when ready to push changes:
4. *git checkout* *version-name* and *git pull* changes.
5. *git checkout* *v-work* and *git merge* with *version-name* (use *mergetool* on conflicts.)
6. *git checkout* *version-name* and *git merge --squash*

Conclusion
==========

*Branches* and *tags* are great tools to manage versions in git_. Just use them.

References
==========

.. _`git scm`: https://git-scm.com/

.. _git: https://git-scm.com/

   | git: `git scm`_
   